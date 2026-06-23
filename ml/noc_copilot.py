#!/usr/bin/env python3
"""
PS13 NOC Copilot — FastAPI server for ML-predictive SD-WAN monitoring.

Combines 7-model ensemble predictor, Ollama LLM (Qwen3:8b), and ChromaDB
RAG pipeline into a unified NOC assistant API.

Endpoints:
  GET  /health          — System health (models, LLM, RAG)
  POST /predict         — Full ensemble diagnosis from telemetry snapshot
  POST /explain         — ML diagnosis → natural language explanation
  POST /query           — Natural language NOC query (RAG + LLM)
  GET  /models/status   — Per-model load status
  POST /rag/ingest      — Trigger/check RAG ingestion
  POST /rag/query       — Direct vector search
"""

from __future__ import annotations

import json
import os
import sys
import time
import warnings
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# ── Ensure ml/ is on sys.path ─────────────────────────────────────────
BASE = Path(__file__).resolve().parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from ensemble_predictor import (
    COMMON_FEATURES,
    FAULT_CLASSES_SORTED,
    LSTM_OUTPUTS,
    EnsemblePredictor,
)

# ── Config from env ────────────────────────────────────────────────────
HOST = os.environ.get("NOC_HOST", "0.0.0.0")
PORT = int(os.environ.get("NOC_PORT", "8000"))
MODELS_DIR = os.environ.get("NOC_MODELS_DIR", str(BASE / "models"))
ONNX_DIR = os.environ.get("NOC_ONNX_DIR", str(BASE / "models" / "onnx"))
OLLAMA_BASE_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
LLM_MODEL = os.environ.get("NOC_LLM_MODEL", "qwen3:8b")
USE_LLM = os.environ.get("NOC_ENABLE_LLM", "1") == "1"
USE_RAG = os.environ.get("NOC_ENABLE_RAG", "1") == "1"

# ── FastAPI app ────────────────────────────────────────────────────────
app = FastAPI(
    title="PS13 NOC Copilot",
    version="1.0.0",
    description="ML-predictive NOC assistant for 4-site MPLS SD-WAN",
)

# Allow browser dashboard from any origin (file://, local dev, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Lazy-loaded globals ────────────────────────────────────────────────
_predictor: EnsemblePredictor | None = None
_llm: Any = None
_rag: Any = None


def get_predictor() -> EnsemblePredictor:
    global _predictor
    if _predictor is None:
        _predictor = EnsemblePredictor(
            models_dir=MODELS_DIR,
            onnx_dir=ONNX_DIR,
            device="cpu",
        )
    return _predictor


def get_llm():
    global _llm
    if _llm is None and USE_LLM:
        try:
            from llm_interface import LLMInterface

            _llm = LLMInterface(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)
        except Exception as e:
            print(f"[WARN] LLM not available: {e}")
            _llm = None
    return _llm


def get_rag():
    global _rag
    if _rag is None and USE_RAG:
        try:
            from rag_pipeline import RAGPipeline

            _rag = RAGPipeline()
        except Exception as e:
            print(f"[WARN] RAG not available: {e}")
            _rag = None
    return _rag


# ═══════════════════════════════════════════════════════════════════════════
# Pydantic models
# ═══════════════════════════════════════════════════════════════════════════


class TelemetrySnapshot(BaseModel):
    """Single-point telemetry data matching COMMON_FEATURES."""
    cpu_util_pct: float = 0
    memory_util_pct: float = 0
    interface_bandwidth_util_pct: float = 0
    latency_ms: float = 0
    packet_loss_pct: float = 0
    jitter_ms: float = 0
    tcp_retransmits_pct: float = 0
    bgp_prefix_count: float = 0
    ospf_lsa_count: float = 0
    ldp_label_count: float = 0
    mpls_label_stack_depth: float = 0
    flow_count: float = 0
    # Optional context
    site: str = "unknown"
    device_id: str = "unknown"
    device_role: str = "unknown"
    timestamp: str = ""


class PredictRequest(BaseModel):
    """Full diagnosis request."""
    telemetry: TelemetrySnapshot
    timeseries_history: list[list[float]] | None = None
    per_node_features: dict[str, float] | None = None
    include_llm: bool = Field(default=False, description="Generate LLM explanation")


class ExplainRequest(BaseModel):
    """Request an LLM explanation of existing diagnosis data."""
    diagnosis: dict[str, Any]
    rag_query: str | None = None
    telemetry_snapshot: dict[str, float] | None = None


class QueryRequest(BaseModel):
    """Natural language NOC query."""
    query: str
    ml_context: dict[str, Any] | None = None
    n_rag_results: int = 5


class RAGQueryRequest(BaseModel):
    """Direct vector search query."""
    query: str
    n_results: int = 5
    filter_fault: str | None = None


# ═══════════════════════════════════════════════════════════════════════════
# Helper: build timeseries history from recent telemetry data
# ═══════════════════════════════════════════════════════════════════════════


def _load_recent_timeseries(
    device_id: str | None = None,
    n_hours: int = 24,
) -> np.ndarray:
    """Load recent telemetry data as a numpy sequence for forecast."""
    data_path = Path(TELEMETRY_PATH) if (
        TELEMETRY_PATH := str(BASE / "data" / "telemetry.parquet")
    ) else None
    # Re-evaluate path properly
    _tp = BASE / "data" / "telemetry.parquet"
    if not _tp.exists():
        return np.zeros((12, len(LSTM_OUTPUTS)), dtype=np.float32)

    df = pd.read_parquet(_tp)
    if device_id and device_id != "unknown":
        df = df[df["device_id"] == device_id]
    df = df.tail(n_hours)

    if len(df) == 0:
        return np.zeros((12, len(LSTM_OUTPUTS)), dtype=np.float32)

    cols = [c for c in LSTM_OUTPUTS if c in df.columns]
    if not cols:
        return np.zeros((12, len(LSTM_OUTPUTS)), dtype=np.float32)

    arr = df[cols].values.astype(np.float32)
    return arr


# ═══════════════════════════════════════════════════════════════════════════
# Routes
# ═══════════════════════════════════════════════════════════════════════════


@app.get("/health")
def health_check() -> dict[str, Any]:
    """System health: models, LLM, RAG."""
    pred = get_predictor()

    # Check model load status
    model_status: dict[str, str] = {}
    for name in ["xgboost", "isolation_forest", "autoencoder", "lstm", "gnn", "prophet", "tti_regressor"]:
        m = pred.load_model(name)
        model_status[name] = "loaded" if m is not None else "unavailable"

    # LLM health
    llm_health: dict[str, Any] = {"status": "disabled"}
    llm = get_llm()
    if llm:
        try:
            llm_health = llm.health()
        except Exception as e:
            llm_health = {"status": "error", "error": str(e)}

    # RAG health
    rag_health: dict[str, Any] = {"status": "disabled"}
    rag = get_rag()
    if rag:
        try:
            rag_health = {"status": "ok", "count": rag.count}
        except Exception as e:
            rag_health = {"status": "error", "error": str(e)}

    return {
        "status": "ok",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "llm": llm_health,
        "rag": rag_health,
        "models": model_status,
    }


@app.get("/models/status")
def model_status() -> dict[str, Any]:
    """Per-model load status with engine info."""
    pred = get_predictor()
    status: dict[str, Any] = {}
    for name in ["xgboost", "isolation_forest", "autoencoder", "lstm", "gnn", "prophet", "tti_regressor"]:
        m = pred.load_model(name)
        if m is not None:
            status[name] = {"loaded": True, "engine": m.get("engine", "?")}
        else:
            status[name] = {"loaded": False, "engine": None}

    return {
        "available_models": [k for k, v in status.items() if v["loaded"]],
        "unavailable_models": [k for k, v in status.items() if not v["loaded"]],
        "details": status,
        "warnings": pred._warnings[-5:] if pred._warnings else [],
    }


@app.post("/predict")
def predict(request: PredictRequest) -> dict[str, Any]:
    """Run full ensemble diagnosis on telemetry snapshot."""
    pred = get_predictor()
    tele = request.telemetry

    # Build feature vector
    feature_vector = np.array(
        [
            tele.cpu_util_pct,
            tele.memory_util_pct,
            tele.interface_bandwidth_util_pct,
            tele.latency_ms,
            tele.packet_loss_pct,
            tele.jitter_ms,
            tele.tcp_retransmits_pct,
            tele.bgp_prefix_count,
            tele.ospf_lsa_count,
            tele.ldp_label_count,
            tele.mpls_label_stack_depth,
            tele.flow_count,
        ],
        dtype=np.float32,
    )

    # Timeseries history
    if request.timeseries_history is not None and len(request.timeseries_history) > 0:
        ts_history = np.array(request.timeseries_history, dtype=np.float32)
    else:
        ts_history = _load_recent_timeseries(tele.device_id)

    # Current telemetry as DataFrame
    current_df = pd.DataFrame([{
        **{f: getattr(tele, f) for f in COMMON_FEATURES},
        "device_id": tele.device_id,
        "site": tele.site,
        "device_role": tele.device_role,
        "timestamp": tele.timestamp or time.strftime("%Y-%m-%dT%H:%M:%S"),
    }])

    # Timestamp features (for GNN / Prophet)
    ts_features: dict[str, Any] = {
        "timestamp": tele.timestamp or time.strftime("%Y-%m-%dT%H:%M:%S"),
        "device_id": tele.device_id,
    }
    if request.per_node_features:
        ts_features.update(request.per_node_features)

    # Run all 3 prediction pipelines
    start = time.time()

    fault = pred.predict_fault(feature_vector.reshape(1, -1), ts_features)
    timeseries = pred.predict_timeseries(ts_history)
    tti = pred.predict_tti(feature_vector.reshape(1, -1))

    elapsed = round(time.time() - start, 3)

    result: dict[str, Any] = {
        "timestamp": tele.timestamp or time.strftime("%Y-%m-%dT%H:%M:%S"),
        "device_id": tele.device_id,
        "site": tele.site,
        "inference_time_ms": round(elapsed * 1000),
        "fault_detection": fault,
        "timeseries_forecast": timeseries,
        "tti_estimate": tti,
    }

    # Optionally include LLM explanation
    if request.include_llm and USE_LLM:
        llm = get_llm()
        rag = get_rag()
        if llm:
            rag_context = None
            if rag and not request.include_llm:
                try:
                    rag_context = rag.get_rag_context(
                        f"{tele.device_id} {tele.site} telemetry",
                        n_results=3,
                    )
                except Exception:
                    pass
            try:
                explanation = llm.explain_diagnosis(
                    diagnosis=result,
                    rag_context=rag_context,
                    telemetry_snapshot=feature_vector.tolist(),
                )
                result["llm_explanation"] = explanation
            except Exception as e:
                result["llm_explanation"] = f"LLM error: {e}"

    return result


@app.post("/explain")
def explain(request: ExplainRequest) -> dict[str, Any]:
    """Generate natural-language explanation of an ML diagnosis."""
    llm = get_llm()
    if not llm:
        error_msg = "LLM is not available. Install Ollama and pull qwen3:8b."
        return {"status": "error", "error": error_msg}

    rag = get_rag()
    rag_context = None
    if rag and request.rag_query:
        try:
            rag_context = rag.get_rag_context(request.rag_query, n_results=3)
        except Exception:
            pass

    try:
        explanation = llm.explain_diagnosis(
            diagnosis=request.diagnosis,
            rag_context=rag_context,
            telemetry_snapshot=request.telemetry_snapshot,
        )
        return {"status": "ok", "explanation": explanation}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.post("/query")
def query(request: QueryRequest) -> dict[str, Any]:
    """Natural-language NOC query with RAG + ML context."""
    llm = get_llm()
    if not llm:
        return {"status": "error", "error": "LLM not available"}

    rag = get_rag()
    rag_context = None
    if rag:
        try:
            rag_context = rag.get_rag_context(
                request.query,
                n_results=request.n_rag_results,
            )
        except Exception:
            pass

    try:
        answer = llm.answer_query(
            user_query=request.query,
            rag_context=rag_context,
            ml_context=request.ml_context,
        )
        return {
            "status": "ok",
            "query": request.query,
            "answer": answer,
            "rag_context": rag_context,
            "rag_enabled": rag is not None,
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.post("/rag/ingest")
def rag_ingest() -> dict[str, Any]:
    """Trigger RAG ingestion of telemetry data."""
    rag = get_rag()
    if not rag:
        return {"status": "error", "error": "RAG not available"}
    try:
        result = rag.ingest_telemetry()
        return result
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.post("/rag/query")
def rag_query(request: RAGQueryRequest) -> dict[str, Any]:
    """Direct vector search over historical telemetry."""
    rag = get_rag()
    if not rag:
        return {"status": "error", "error": "RAG not available"}
    try:
        if request.filter_fault:
            result = rag.query_by_fault(request.filter_fault, n_results=request.n_results)
        else:
            result = rag.query(request.query, n_results=request.n_results)
        return {"status": "ok", "results": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/rag/stats")
def rag_stats() -> dict[str, Any]:
    """RAG collection statistics."""
    rag = get_rag()
    if not rag:
        return {"status": "error", "error": "RAG not available"}
    try:
        return {"status": "ok", "count": rag.count}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ═══════════════════════════════════════════════════════════════════════════
# Startup event: preload models + warm
# ═══════════════════════════════════════════════════════════════════════════


@app.on_event("startup")
def startup() -> None:
    print("=" * 60)
    print("  PS13 NOC Copilot — Starting up")
    print("=" * 60)

    # Preload predictor
    pred = get_predictor()
    loaded: list[str] = []
    failed: list[str] = []
    for name in ["xgboost", "isolation_forest", "prophet", "tti_regressor", "autoencoder", "lstm", "gnn"]:
        m = pred.load_model(name)
        if m is not None:
            loaded.append(name)
        else:
            failed.append(name)
    print(f"  Models loaded: {loaded}")
    if failed:
        print(f"  Models unavailable (offline-only): {failed}")
    if pred._warnings:
        for w in pred._warnings[-3:]:
            print(f"  [WARN] {w}")

    # Test LLM
    if USE_LLM:
        llm = get_llm()
        if llm:
            try:
                health = llm.health()
                print(f"  LLM ({llm.model}): {health.get('status')} "
                      f"({health.get('latency_ms', '?')}ms)")
            except Exception as e:
                print(f"  LLM: not available ({e})")
        else:
            print("  LLM: disabled (import failed)")
    else:
        print("  LLM: disabled by NOC_ENABLE_LLM=0")

    # Test RAG & auto-ingest if empty
    if USE_RAG:
        rag = get_rag()
        if rag:
            count = rag.count
            print(f"  RAG (ChromaDB): {count} docs indexed")
            if count == 0:
                print("  RAG: auto-ingesting telemetry data...")
                try:
                    result = rag.ingest_telemetry()
                    print(f"  RAG: ingested {result.get('indexed', 0)} docs "
                          f"({result.get('elapsed_seconds', 0):.1f}s)")
                except Exception as e:
                    print(f"  RAG: auto-ingest failed ({e})")
        else:
            print("  RAG: disabled (import failed)")
    else:
        print("  RAG: disabled by NOC_ENABLE_RAG=0")

    print(f"  Server: http://{HOST}:{PORT}")
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════


def main() -> None:
    uvicorn.run(
        "noc_copilot:app",
        host=HOST,
        port=PORT,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()
