---
created: 2026-06-23
tags: [ps13, deployment, server, startup]
---

# Server Startup — 3-Terminal Setup

## Architecture

```
Terminal 1                  Terminal 2                  Terminal 3
┌─────────────┐            ┌──────────────┐            ┌──────────────┐
│  ollama serve│ ──HTTP──▶ │  uvicorn     │ ◀──REST── │  Browser     │
│  (qwen3:8b)  │   :11434  │  FastAPI app │   :8000   │  Dashboard   │
│  nomic-embed │           │  7 endpoints │           │  .html file  │
└─────────────┘            │  RAG auto-   │           └──────────────┘
                           │  ingest      │
                           └──────────────┘
```

## Step 1 — Ollama (LLM + Embeddings)

```bash
ollama serve
# Pull models if needed:
ollama pull qwen3:8b      # 5.2 GB - main LLM
ollama pull nomic-embed-text  # 274 MB - RAG embeddings
```

**Verify**: `curl http://localhost:11434/api/tags` → shows loaded models

## Step 2 — FastAPI Server

```bash
cd /home/ego/Documents/ISRO2026
ml/venv/bin/python -m uvicorn ml.noc_copilot:app --host 0.0.0.0 --port 8000
```

| Env Var | Default | Purpose |
|---------|---------|---------|
| `NOC_LLM_MODEL` | `qwen3:8b` | Ollama model |
| `NOC_MAX_TOKENS` | `4096` | Generation length |
| `NOC_TEMPERATURE` | `0.7` | Creativity |
| `NOC_ENABLE_LLM` | `1` | Disable for faster testing |
| `NOC_ENABLE_RAG` | `1` | Disable if no vectordb |

**First startup**: Auto-ingests 7,920 RAG docs (~105s)

**Verify**: `curl http://localhost:8000/health` → `{"status": "healthy", "models": "7/7", "llm_latency_ms": 295, "rag_docs": 7920}`

## Step 3 — Dashboard

```bash
xdg-open /home/ego/Documents/ISRO2026/ml/noc-dashboard.html
```

Or open in browser directly: `file:///home/ego/Documents/ISRO2026/ml/noc-dashboard.html`

## Notes

- Shell: Use `ml/venv/bin/python` NOT `source activate` (shell compatibility)
- CWD must be project root for `ml.` module resolution
- Ollama auto-starts if systemd service is enabled (`sudo systemctl start ollama`)

## Related

- [[noc-copilot]] — What runs on the server
- [[air-gap-validation]] — Offline verification
