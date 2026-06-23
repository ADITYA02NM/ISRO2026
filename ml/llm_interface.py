#!/usr/bin/env python3
"""
LLM Interface for PS13 NOC Copilot.

Wraps Ollama (Qwen3:8b / Gemma3:12b) with NOC-operator system prompts.
Provides structured query, explanation, and diagnosis generation
for the NOC Copilot FastAPI server.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OLLAMA_BASE_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
LLM_MODEL = os.environ.get("NOC_LLM_MODEL", "qwen3:8b")
MAX_TOKENS = int(os.environ.get("NOC_MAX_TOKENS", "1024"))
TEMPERATURE = float(os.environ.get("NOC_TEMPERATURE", "0.7"))

NOC_SYSTEM_PROMPT = """You are a senior NOC (Network Operations Center) engineer assistant for a multi-site MPLS SD-WAN network spanning 4 cities: Bangalore (BLR), Mumbai (MUM), Chennai (CHE), and Delhi (DEL). Your network has 11 devices across core (P), provider-edge (PE), and customer-edge (CE) roles.

Your job is to analyse network telemetry, diagnose faults, explain ML model predictions, and recommend remediation actions.

Rules:
- Be concise and technical. Use network engineering terminology.
- When explaining predictions, cite the specific metrics that triggered the alert.
- Provide actionable remediation steps when a fault is detected.
- When uncertain, state confidence levels from the ML ensemble.
- Reference historical incidents from the RAG context when available.
- Format responses with clear sections: Diagnosis, Root Cause, Confidence, Recommended Action."""

DEFAULT_REQUEST_TIMEOUT = 120


# ---------------------------------------------------------------------------
# LLM Interface
# ---------------------------------------------------------------------------


class LLMInterface:
    """Ollama-based LLM wrapper for NOC Copilot."""

    def __init__(
        self,
        model: str = LLM_MODEL,
        base_url: str = OLLAMA_BASE_URL,
        system_prompt: str | None = None,
    ) -> None:
        import ollama

        self._client = ollama.Client(host=base_url)
        self._model = model
        self._system_prompt = system_prompt or NOC_SYSTEM_PROMPT

    # ── Properties ────────────────────────────────────────────────────────

    @property
    def model(self) -> str:
        return self._model

    # ── Core generation ───────────────────────────────────────────────────

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
        stream: bool = False,
    ) -> str:
        """Generate a response from the LLM."""
        messages = [
            {"role": "system", "content": system_prompt or self._system_prompt},
            {"role": "user", "content": prompt},
        ]
        start = time.time()
        resp = self._client.chat(
            model=self._model,
            messages=messages,
            options={
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            stream=stream,
        )
        elapsed = time.time() - start
        content = resp["message"]["content"] if not stream else self._stream_response(resp)
        return content.strip()

    @staticmethod
    def _stream_response(resp) -> str:
        """Collate streaming response chunks."""
        parts: list[str] = []
        for chunk in resp:
            parts.append(chunk["message"]["content"])
        return "".join(parts)

    # ── Structured prompts ────────────────────────────────────────────────

    def explain_diagnosis(
        self,
        diagnosis: dict[str, Any],
        rag_context: str | None = None,
        telemetry_snapshot: dict[str, float] | None = None,
    ) -> str:
        """Generate a natural-language explanation of an ML diagnosis."""
        parts = ["## Current Telemetry Snapshot"]
        if telemetry_snapshot:
            parts.append(json.dumps(telemetry_snapshot, indent=2))
        else:
            parts.append("(not provided)")

        parts.append("\n## ML Ensemble Diagnosis")
        parts.append(json.dumps(diagnosis, indent=2))

        if rag_context:
            parts.append(f"\n## Historical Context\n{rag_context}")

        prompt = (
            "You are a NOC engineer reviewing an ML-based network diagnosis.\n"
            "Explain what is happening in plain technical language.\n"
            "Structure your response:\n"
            "1. **Status** — is there a fault? What type? Severity?\n"
            "2. **Key Indicators** — which metrics triggered the alert\n"
            "3. **Root Cause Assessment** — likely cause based on symptoms\n"
            "4. **Confidence** — how reliable is this diagnosis?\n"
            "5. **Recommended Action** — what should the NOC operator do?\n\n"
            + "\n".join(parts)
        )
        return self.generate(prompt)

    def analyse_timeseries(
        self,
        forecast: dict[str, Any],
        rag_context: str | None = None,
    ) -> str:
        """Analyse a time-series forecast for operator insights."""
        parts = ["## ML Timeseries Forecast"]
        parts.append(json.dumps(forecast, indent=2))
        if rag_context:
            parts.append(f"\n## Historical Context\n{rag_context}")

        prompt = (
            "You are a NOC engineer reviewing a network telemetry forecast.\n"
            "Analyse the predicted trends and flag any concerns.\n"
            "Structure your response:\n"
            "1. **Trend Summary** — what metrics are rising/falling?\n"
            "2. **Anomaly Risk** — is any forecast approaching critical thresholds?\n"
            "3. **Proactive Recommendation** — what should be done before issues escalate?\n\n"
            + "\n".join(parts)
        )
        return self.generate(prompt, max_tokens=768)

    def answer_query(
        self,
        user_query: str,
        rag_context: str | None = None,
        ml_context: dict[str, Any] | None = None,
    ) -> str:
        """Answer an arbitrary NOC question using RAG context + ML state."""
        parts = ["## User Question", user_query]
        if ml_context:
            parts.append("\n## Current ML Analysis")
            parts.append(json.dumps(ml_context, indent=2))
        if rag_context:
            parts.append(f"\n## Historical Context\n{rag_context}")

        prompt = (
            "Answer the NOC operator's question using the provided context.\n"
            "Be technical and concise.\n"
            "If the answer is not in the context, say so clearly.\n\n"
            + "\n".join(parts)
        )
        return self.generate(prompt)

    def generate_incident_report(
        self,
        diagnosis: dict[str, Any],
        rag_context: str | None = None,
    ) -> str:
        """Generate a structured incident report from ML diagnosis."""
        parts = []
        if rag_context:
            parts.append(f"## Historical Context\n{rag_context}")
        parts.append("## ML Diagnosis Data\n" + json.dumps(diagnosis, indent=2))

        prompt = (
            "Generate a structured incident report in this format:\n\n"
            "## Incident Report\n"
            "**Timestamp:** ...\n"
            "**Affected Site(s):** ...\n"
            "**Fault Type:** ...\n"
            "**Severity:** ...\n"
            "**Description:** ...\n"
            "**Root Cause Hypothesis:** ...\n"
            "**Confidence:** ...\n"
            "**RecommendedActions:** ...\n"
            "**Related Historical Incidents:** (if any)\n\n"
            + "\n".join(parts)
        )
        return self.generate(prompt, temperature=0.3, max_tokens=1536)

    # ── Utility ───────────────────────────────────────────────────────────

    def health(self) -> dict[str, Any]:
        """Check if the LLM is reachable and responsive."""
        start = time.time()
        try:
            resp = self._client.chat(
                model=self._model,
                messages=[
                    {"role": "system", "content": "Respond with exactly: OK"},
                    {"role": "user", "content": "ping"},
                ],
                options={"num_predict": 10, "temperature": 0},
            )
            elapsed = time.time() - start
            return {
                "status": "ok",
                "model": self._model,
                "latency_ms": round(elapsed * 1000),
                "response": resp["message"]["content"].strip(),
            }
        except Exception as e:
            return {
                "status": "error",
                "model": self._model,
                "error": str(e),
            }


# ═══════════════════════════════════════════════════════════════════════════
# CLI test
# ═══════════════════════════════════════════════════════════════════════════


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="PS13 LLM Interface — Test")
    parser.add_argument("--prompt", type=str, default="What network metrics should I check?", help="Query prompt")
    parser.add_argument("--model", type=str, default=LLM_MODEL, help="Ollama model")
    args = parser.parse_args()

    llm = LLMInterface(model=args.model)
    print(f"Model: {llm.model}")
    print(f"Health: {llm.health()}\n")
    print("Response:")
    print(llm.generate(args.prompt))


if __name__ == "__main__":
    main()
