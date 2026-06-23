---
created: 2026-06-23
tags: [ps13, phase-04, llm, rag, chromadb, ollama, completed]
status: completed
---

# Phase 4: Offline LLM + RAG Pipeline

**Status: ✅ COMPLETED — Ollama + ChromaDB + LangChain-free RAG**

**Goal:** Build a fully offline LLM inference pipeline with Retrieval-Augmented Generation (RAG) — NO internet access required once installed.

---

## Components

### 1. Ollama (Local LLM Server)

| Property | Value |
|----------|-------|
| **Binary** | `/usr/local/bin/ollama` v0.24.0 |
| **Models** | `qwen3:8b` (5.2 GB) + `gemma3:12b` (8.1 GB) |
| **API Port** | 11434 (localhost only) |
| **Context** | Qwen3: 128K tokens |

### 2. ChromaDB (Vector Database)

| Property | Value |
|----------|-------|
| **Persistence** | `ml/vectordb/` directory |
| **Embedding** | Ollama `qwen3:8b` embeddings (3840-dim) |
| **Collection** | `telemetry_incidents` |
| **Documents** | ~7,920 telemetry records converted to natural language |

### 3. RAG Pipeline — `ml/rag_pipeline.py` (330 lines)

**Class: `RAGPipeline`**

| Method | Function |
|--------|----------|
| `ingest_telemetry(df)` | Converts each telemetry row → natural-language doc → upsert to ChromaDB |
| `query(text, n=5)` | Semantic search — finds most relevant past incidents |
| `query_by_fault(fault_type, n=5)` | Filtered search by fault category |
| `query_similar_incidents(snapshot, n=5)` | Converts snapshot to text → vector search |
| `get_rag_context(text, n=5)` | Returns formatted "Context:" block for LLM prompt |
| `reset()` | Deletes all documents from collection |

**Document format:**
```
[TIMESTAMP] Site: BLR | Device: PE1-BLR (PE) | Fault: BGP Flap (None)
  CPU: 45.2% | MEM: 62.1% | BW: 38.7% | Loss: 0.12% | Latency: 4.23ms
  Jitter: 0.89ms | TCP Retrans: 1.23 | Queue: 3 | Interface Errors: 0.02
  BGP: 142 prefixes | OSPF: 34 LSAs | MPLS: 28 LSPs
```

### 4. LLM Interface — `ml/llm_interface.py` (260 lines)

**Class: `LLMInterface`**

| Method | Function |
|--------|----------|
| `generate(prompt, system=None)` | Raw Ollama generate call |
| `explain_diagnosis(prediction, snapshot)` | Explains ML prediction in plain English |
| `analyse_timeseries(series)` | Trend analysis + anomaly description |
| `answer_query(query, rag_context)` | RAG-augmented Q&A |
| `generate_incident_report(prediction)` | Structured incident report |
| `health()` | Checks Ollama reachability + model availability |

**System prompt:** Senior NOC engineer persona — ISRO PS13 MPLS SD-WAN, 4-city network.

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `NOC_LLM_MODEL` | `qwen3:8b` | Ollama model for generation |
| `NOC_MAX_TOKENS` | 1024 | Max response length |
| `NOC_TEMPERATURE` | 0.3 | Low temp = factual answers |
| `NOC_ENABLE_LLM` | `1` | Toggle LLM on/off |
| `NOC_ENABLE_RAG` | `1` | Toggle RAG on/off |
| `NOC_EMBED_MODEL` | `qwen3:8b` | Ollama model for embeddings |

---

## Startup (Auto-Ingest)

On server startup, `noc_copilot.py` checks `RAGPipeline().count()`:
- If **0** → auto-runs `ingest_telemetry()` from `ml/data/telemetry.parquet`
- If **>0** → skips (preserves existing data across restarts)

---

## Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Embedding model | qwen3:8b (not separate embedding model) | Save disk space, single model to serve |
| Vector DB | ChromaDB | Zero dependencies, persistent, local-only |
| RAG without LangChain | Direct ChromaDB API | Avoid dependency chain, simpler debugging |
| Document granularity | Per-row (not per-incident) | Max context flexibility; retrieval groups similar rows |
