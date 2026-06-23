---
created: 2026-06-23
tags: [ps13, server, fastapi, core]
---

# NOC Copilot — `ml/noc_copilot.py`

**531 lines.** FastAPI server that unifies ML predictions, RAG context, and LLM chat into a REST API consumed by the 3D dashboard.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | All models loaded? LLM reachable? RAG doc count? |
| `GET` | `/models/status` | Per-model engine + load status |
| `POST` | `/predict` | Full diagnosis: fault + anomaly + TTI + forecast + graph |
| `POST` | `/explain` | Raw diagnosis → natural language via LLM |
| `POST` | `/query` | Natural language NOC question → RAG context → LLM answer |
| `POST` | `/rag/ingest` | Trigger ChromaDB re-ingestion (~105s for 7,920 docs) |
| `POST` | `/rag/query` | Direct vector similarity search |
| `GET` | `/rag/stats` | ChromaDB document count |

## Startup Sequence

```
1. Import: EnsemblePredictor, LLMInterface, RAGPipeline
2. Preload all 7 models (try ONNX → torch → native)
3. Check Ollama LLM health
4. Auto-ingest RAG if vectordb is empty
5. Print startup banner with model/LLM/RAG status
```

## CORS

CORS middleware allows browser access from any origin (dashboard connects on `localhost:8000`).

## Predict Request Flow

```
POST /predict { telemetry: TelemetrySnapshot }
  → predictor.predict(snapshot) 
    → feature engineering (109-dim)
    → fault classification (xgboost)
    → anomaly scoring (isolation_forest)
    → TTI regression (tti_regressor)
    → time-series forecast (lstm + prophet + autoencoder)
    → graph anomaly (gnn)
  → returns PredictResult (dict)
```

## Query Request Flow

```
POST /query { question: str }
  → rag.query(question) → 5 nearest docs from ChromaDB
  → llm.answer_query(question, context) → Ollama response
```

## Related

- [[ensemble-predictor]] — Core ML engine this server wraps
- [[rag-pipeline]] — ChromaDB vector search for context
- [[llm-interface]] — Ollama client for generation
- [[noc-dashboard]] — The 3D browser dashboard
- [[server-startup]] — How to start the server
