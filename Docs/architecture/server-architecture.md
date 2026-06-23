---
created: 2026-06-23
tags: [ps13, architecture, server]
---

# Server Architecture

## Component Diagram

```
┌───────────┐     ┌──────────────────────────────────────────┐
│  Browser  │     │         FastAPI Server (:8000)            │
│           │◄────┤                                          │
│ Dashboard │     │  ┌────────────────────────────────────┐  │
│ (Three.js)│     │  │  Router Layer                      │  │
│           │     │  │  /health  /predict  /explain        │  │
│           │     │  │  /query   /rag/*    /models/*       │  │
└───────────┘     │  └──────────┬─────────────────────────┘  │
                  │             │                             │
                  │  ┌──────────▼────────────────────────┐    │
                  │  │  Service Layer (Lazy-Loaded)       │    │
                  │  │                                    │    │
                  │  │  ┌────────────┐ ┌──────────────┐   │    │
                  │  │  │Ensemble    │ │LLMInterface  │   │    │
                  │  │  │Predictor   │ │(Ollama)      │   │    │
                  │  │  │(7 models)  │ └──────┬───────┘   │    │
                  │  │  └────────────┘        │           │    │
                  │  │  ┌────────────┐        │           │    │
                  │  │  │RAGPipeline │        │           │    │
                  │  │  │(ChromaDB)  │        │           │    │
                  │  │  └────────────┘        │           │    │
                  │  └────────────────────────┼──────────┘    │
                  └──────────────────────────┼───────────────┘
                                             │
                  ┌──────────────────────────┼───────────────┐
                  │            ┌──────────────▼───────────┐  │
                  │            │    Ollama Server (:11434)  │  │
                  │            │  qwen3:8b / gemma3:12b     │  │
                  │            └────────────────────────────┘  │
                  │                                          │
                  │          ChromaDB (ml/vectordb/)          │
                  │          ~7,920 telemetry documents       │
                  └──────────────────────────────────────────┘
```

## Module Dependencies

```
noc_copilot.py (FastAPI app)
  ├── ensemble_predictor.py
  │   ├── models/xgboost_model.py
  │   ├── models/isolation_forest_model.py
  │   ├── models/tti_regressor_model.py
  │   ├── models/prophet_model.py
  │   ├── models/autoencoder_model.py
  │   ├── models/lstm_model.py
  │   └── models/gnn_model.py
  ├── llm_interface.py
  │   └── ollama (Python SDK)
  └── rag_pipeline.py
      └── chromadb (Python SDK)
```

## Request Lifecycle: POST /predict

```
1. Client sends TelemetrySnapshot (JSON, 16 fields)
2. Router validates with Pydantic (BaseModel)
3. Server passes snapshot to EnsemblePredictor
4. Predictor runs feature_engineering() → 109 features
5. Each model predicts (parallel via model list loop)
6. Results aggregated into DiagnosisResult dict
7. If explain=True → LLMInterface.explain_diagnosis() called
8. JSON response returned to client
```

## Request Lifecycle: POST /query

```
1. Client sends {"question": "Why is BLR having packet loss?"}
2. Server queries RAGPipeline.get_rag_context(question) → 5 similar docs
3. Server calls LLMInterface.answer_query(question, context)
4. Ollama generates answer with RAG context + NOC system prompt
5. Streamed/generated response returned to client
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `NOC_LLM_MODEL` | `qwen3:8b` | Ollama inference model |
| `NOC_EMBED_MODEL` | `qwen3:8b` | Ollama embedding model |
| `NOC_MAX_TOKENS` | 1024 | Max generation tokens |
| `NOC_TEMPERATURE` | 0.3 | Response creativity |
| `NOC_ENABLE_LLM` | 1 | Enable LLM features |
| `NOC_ENABLE_RAG` | 1 | Enable RAG retrieval |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
