---
created: 2026-06-23
tags: [ps13, rag, chromadb, embeddings]
---

# RAG Pipeline — `ml/rag_pipeline.py`

**330 lines.** ChromaDB-based vector retrieval augmented generation pipeline for NOC query context.

## Architecture

```
telemetry.parquet (7,920 rows)
  ↓
ingest_telemetry()
  → each row → natural-language document
  → embed via Ollama (nomic-embed-text, 274 MB model)
  → store in ChromaDB (ml/vectordb/)
  ↓
query()
  → embed query via Ollama
  → cosine similarity search
  → return top 5 nearest documents with metadata
```

## Embedding Note

**qwen3:8b does NOT support `/api/embeddings`.** The server automatically pulls and uses `nomic-embed-text` for the embedding function. This is a 274 MB model that runs locally in Ollama.

## Document Schema

Each telemetry row becomes a document like:
```
"[TIMESTAMP] Device {device_id} ({device_role}) at {site}
  Status: Metrics {latency:.1f}ms, jitter {jitter:.1f}ms, 
  packet_loss {packet_loss:.2f}%, throughput {throughput:.1f}Mbps...
  Fault: {fault_type} (severity {fault_severity})"
```

**Metadata**: `site`, `device_id`, `device_role`, `fault_type`, `fault_severity`, `timestamp`

## Ingestion

- Auto-ingests when server starts if vectordb is empty
- 7,920 docs in ~105 seconds
- Vector DB stored at `ml/vectordb/` (persistent ChromaDB client)

## Query Methods

| Method | Purpose |
|--------|---------|
| `query(text, n_results=5)` | General semantic search |
| `query_by_fault(fault_type)` | Filter by fault type metadata |
| `query_similar_incidents(device_id, hours=24)` | Similar past incidents for a device |
| `get_rag_context(text)` | Get formatted context string for LLM prompts |
| `reset()` | Wipe and recreate collection |

## Related

- [[llm-interface]] — Uses RAG context for Q&A
- [[noc-copilot]] — Exposes RAG as HTTP endpoints
- [[telemetry-schema]] — The source data
