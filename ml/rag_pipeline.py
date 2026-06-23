#!/usr/bin/env python3
"""
RAG Pipeline for PS13 NOC Copilot.

Ingests telemetry data into ChromaDB with Ollama embeddings,
enables semantic search over historical network incidents,
and provides context retrieval for LLM-augmented diagnosis.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Optional

import chromadb
import numpy as np
import pandas as pd
from chromadb.config import Settings

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE = Path(__file__).resolve().parent
VECTORDB_DIR = BASE / "vectordb"
TELEMETRY_PATH = BASE / "data" / "telemetry.parquet"
CHUNK_SIZE = 200  # rows per document for vectorisation

OLLAMA_BASE_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = os.environ.get("NOC_EMBED_MODEL", "nomic-embed-text")
LLM_MODEL = os.environ.get("NOC_LLM_MODEL", "qwen3:8b")

COLLECTION_NAME = "noc_telemetry"

# ---------------------------------------------------------------------------
# Embedding function via Ollama
# ---------------------------------------------------------------------------


class OllamaEmbeddingFunction(chromadb.EmbeddingFunction):
    """ChromaDB-compatible embedding function using Ollama."""

    def __init__(self, model: str = EMBED_MODEL, base_url: str = OLLAMA_BASE_URL) -> None:
        import ollama

        self._ollama = ollama.Client(host=base_url)
        self._model = model

    def __call__(self, input: list[str]) -> list[list[float]]:
        embeddings: list[list[float]] = []
        for text in input:
            resp = self._ollama.embeddings(model=self._model, prompt=text)
            embeddings.append(resp["embedding"])
        return embeddings


# ---------------------------------------------------------------------------
# RAG Pipeline
# ---------------------------------------------------------------------------


class RAGPipeline:
    """Ingests telemetry into ChromaDB and provides semantic retrieval."""

    def __init__(
        self,
        persist_dir: str | Path = VECTORDB_DIR,
        collection_name: str = COLLECTION_NAME,
        embed_model: str = EMBED_MODEL,
    ) -> None:
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        self._client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=Settings(anonymized_telemetry=False),
        )
        self._embed_fn = OllamaEmbeddingFunction(model=embed_model)

        # Get or create collection
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=self._embed_fn,
            metadata={"hnsw:space": "cosine"},
        )

    # ── Properties ────────────────────────────────────────────────────────

    @property
    def collection(self):
        return self._collection

    @property
    def count(self) -> int:
        return self._collection.count()

    # ── Ingest ────────────────────────────────────────────────────────────

    def ingest_telemetry(
        self,
        path: str | Path = TELEMETRY_PATH,
        batch_size: int = 100,
    ) -> dict[str, Any]:
        """Read telemetry parquet and index into ChromaDB."""
        df = pd.read_parquet(path)
        total = len(df)
        print(f"[RAG] Loaded {total} telemetry rows from {path}")

        existing = self.count
        if existing >= total:
            print(f"[RAG] Already indexed {existing}/{total} — skipping ingest")
            return {"status": "skipped", "indexed": existing, "total": total}

        start = time.time()
        indexed = 0
        ids: list[str] = []
        docs: list[str] = []
        metadatas: list[dict[str, Any]] = []

        for idx, row in df.iterrows():
            doc_id = f"tel_{row['timestamp']}_{row['device_id']}"
            if existing > 0 and self._collection.get(ids=[doc_id]).get("ids"):
                continue

            doc_text = self._row_to_document(row)
            doc_meta = self._row_to_metadata(row)

            ids.append(doc_id)
            docs.append(doc_text)
            metadatas.append(doc_meta)

            if len(ids) >= batch_size:
                self._collection.add(ids=ids, documents=docs, metadatas=metadatas)
                indexed += len(ids)
                ids, docs, metadatas = [], [], []

            if (idx + 1) % 2000 == 0:
                elapsed = time.time() - start
                print(f"[RAG] Indexed {idx+1}/{total} rows ({elapsed:.1f}s)")

        if ids:
            self._collection.add(ids=ids, documents=docs, metadatas=metadatas)
            indexed += len(ids)

        elapsed = time.time() - start
        print(f"[RAG] Done — {indexed} new docs indexed in {elapsed:.1f}s")
        return {
            "status": "ok",
            "indexed": indexed,
            "total": self.count,
            "elapsed_seconds": round(elapsed, 2),
        }

    @staticmethod
    def _row_to_document(row: pd.Series) -> str:
        """Convert a telemetry row to a natural-language document."""
        return (
            f"Device {row.get('device_id', '?')} at site {row.get('site', '?')} "
            f"({row.get('device_role', '?')}) at {row.get('timestamp', '?')} — "
            f"CPU: {row.get('cpu_util_pct', 0):.1f}%, "
            f"Memory: {row.get('memory_util_pct', 0):.1f}%, "
            f"Bandwidth: {row.get('interface_bandwidth_util_pct', 0):.1f}%, "
            f"Latency: {row.get('latency_ms', 0):.2f}ms, "
            f"Packet Loss: {row.get('packet_loss_pct', 0):.2f}%, "
            f"Jitter: {row.get('jitter_ms', 0):.2f}ms, "
            f"BGP Prefixes: {row.get('bgp_prefix_count', 0)}, "
            f"OSPF LSAs: {row.get('ospf_lsa_count', 0)}, "
            f"LDP Labels: {row.get('ldp_label_count', 0)}, "
            f"MPLS Stack Depth: {row.get('mpls_label_stack_depth', 0)}, "
            f"TCP Retransmits: {row.get('tcp_retransmits_pct', 0):.2f}%, "
            f"Flow Count: {row.get('flow_count', 0)}, "
            f"Fault: {row.get('fault_type', 'none')} "
            f"(severity {row.get('fault_severity', 0)}), "
            f"TTI: {row.get('time_to_incident_hours', 0):.1f}h"
        )

    @staticmethod
    def _row_to_metadata(row: pd.Series) -> dict[str, Any]:
        """Extract structured metadata from a telemetry row."""
        return {
            "timestamp": str(row.get("timestamp", "")),
            "device_id": str(row.get("device_id", "")),
            "site": str(row.get("site", "")),
            "device_role": str(row.get("device_role", "")),
            "fault_type": str(row.get("fault_type", "none")),
            "fault_severity": int(row.get("fault_severity", 0)),
            "hour": int(row.get("hour", 0)),
            "latency_ms": float(row.get("latency_ms", 0)),
            "packet_loss_pct": float(row.get("packet_loss_pct", 0)),
            "cpu_util_pct": float(row.get("cpu_util_pct", 0)),
            "bandwidth_util": float(row.get("interface_bandwidth_util_pct", 0)),
        }

    # ── Query ─────────────────────────────────────────────────────────────

    def query(
        self,
        query_text: str,
        n_results: int = 5,
        filter_dict: dict | None = None,
    ) -> dict[str, Any]:
        """Semantic search over telemetry."""
        where = filter_dict or None
        results = self._collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where,
        )
        return {
            "query": query_text,
            "n_results": n_results,
            "documents": results.get("documents", [[]])[0],
            "metadatas": results.get("metadatas", [[]])[0],
            "distances": results.get("distances", [[]])[0],
        }

    def query_by_fault(
        self,
        fault_type: str,
        n_results: int = 5,
    ) -> dict[str, Any]:
        """Search past occurrences of a specific fault type."""
        return self.query(
            f"network fault of type {fault_type}",
            n_results=n_results,
            filter_dict={"fault_type": fault_type},
        )

    def query_similar_incidents(
        self,
        telemetry_snapshot: dict[str, float],
        n_results: int = 5,
    ) -> dict[str, Any]:
        """Find historical incidents similar to current telemetry snapshot."""
        desc = (
            f"Device with CPU {telemetry_snapshot.get('cpu_util_pct', 0):.1f}%, "
            f"latency {telemetry_snapshot.get('latency_ms', 0):.2f}ms, "
            f"packet loss {telemetry_snapshot.get('packet_loss_pct', 0):.2f}%"
        )
        return self.query(desc, n_results=n_results)

    # ── Batch query for RAG context ───────────────────────────────────────

    def get_rag_context(
        self,
        query_text: str,
        n_results: int = 5,
    ) -> str:
        """Build a context string from retrieved docs for LLM injection."""
        result = self.query(query_text, n_results=n_results)
        docs = result.get("documents", [])
        if not docs:
            return "No relevant historical data found."

        lines = ["Relevant historical telemetry context:"]
        for i, doc in enumerate(docs, 1):
            meta = result["metadatas"][i - 1] if result.get("metadatas") else {}
            site = meta.get("site", "?")
            device = meta.get("device_id", "?")
            fault = meta.get("fault_type", "?")
            lines.append(f"\n[{i}] Site={site}, Device={device}, Fault={fault}")
            lines.append(f"    {doc}")
        return "\n".join(lines)

    # ── Utility ───────────────────────────────────────────────────────────

    def reset(self) -> None:
        """Delete and recreate the collection."""
        self._client.delete_collection(COLLECTION_NAME)
        self._collection = self._client.create_collection(
            name=COLLECTION_NAME,
            embedding_function=self._embed_fn,
        )
        print(f"[RAG] Collection '{COLLECTION_NAME}' reset")

    def stats(self) -> dict[str, Any]:
        return {"count": self.count, "collection": COLLECTION_NAME}


# ═══════════════════════════════════════════════════════════════════════════
# CLI entry point
# ═══════════════════════════════════════════════════════════════════════════


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="PS13 RAG Pipeline — Ingest & Query")
    parser.add_argument("--ingest", action="store_true", help="Ingest telemetry into ChromaDB")
    parser.add_argument("--query", type=str, help="Semantic search query")
    parser.add_argument("--fault", type=str, help="Search by fault type")
    parser.add_argument("--n", type=int, default=5, help="Number of results")
    parser.add_argument("--reset", action="store_true", help="Reset collection")
    args = parser.parse_args()

    rag = RAGPipeline()

    if args.reset:
        rag.reset()

    if args.ingest:
        result = rag.ingest_telemetry()
        print(json.dumps(result, indent=2))

    if args.query:
        result = rag.query(args.query, n_results=args.n)
        print(f"\nQuery: {args.query}")
        for i, doc in enumerate(result.get("documents", []), 1):
            meta = result["metadatas"][i - 1] if result.get("metadatas") else {}
            print(f"\n  [{i}] Dist={result['distances'][i-1]:.4f} — {meta}")
            print(f"       {doc[:200]}...")

    if args.fault:
        result = rag.query_by_fault(args.fault, n_results=args.n)
        print(f"\nFault: {args.fault} — {len(result.get('documents', []))} results")
        for i, doc in enumerate(result.get("documents", []), 1):
            meta = result["metadatas"][i - 1] if result.get("metadatas") else {}
            print(f"\n  [{i}] Device={meta.get('device_id')} at {meta.get('timestamp')}")
            print(f"       {doc[:200]}...")

    if not any([args.ingest, args.query, args.fault, args.reset]):
        stats = rag.stats()
        print(f"[RAG] Collection: {stats['collection']}, Docs: {stats['count']}")


if __name__ == "__main__":
    main()
