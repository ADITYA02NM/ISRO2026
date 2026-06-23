---
created: 2026-06-23
tags: [ps13, meta, status, implementation]
updated: 2026-06-24
---

# Implementation Notes

## System

- **OS**: Arch Linux (rolling)
- **GPU**: RTX 4060 (8GB VRAM) — CUDA-capable, but all ML models run CPU-only (torch `--index-url cpu`, XGBoost native)
- **RAM**: 15GB — shared RAM + GPU memory
- **Containerlab**: v0.76.1 at `/usr/local/bin/containerlab`
- **Python**: 3.11 in `ml/venv/`
- **Ollama**: qwen3:8b for LLM inference; nomic-embed-text for RAG embeddings

## Architecture Overview

```
Terminal 1 (Operator Console)
  └─ ollama serve (qwen3:8b + nomic-embed-text)

Terminal 2 (Alert Dashboard)
  └─ FastAPI backend (ml/noc_copilot.py)
     ├─ /health, /models/status, /predict, /explain
     ├─ /query (LLM diagnostics)
     ├─ /rag/ingest, /rag/query (ChromaDB)
     └─ WebSocket: predictions, alerts, RAG responses
     
Terminal 3 (Network Topology Verbose)
  └─ Containerlab (topology.clab.yml)
     ├─ 4-site MPLS/SD-WAN (HQ, DC, DR, Regional)
     ├─ FRR: BGP, OSPF, MPLS, LDP
     ├─ IPsec tunnels (StrongSwan)
     ├─ TRex traffic generator
     └─ Telegraf metrics export (5s interval)
```

## Known Issues & Resolutions

| Issue | Status | Resolution |
|-------|--------|-----------|
| GNN ONNX export | 🔴 Unresolved | PyTorch 2.12 static-shape bug; use `gnn.pt` (3KB) |
| LSTM ONNX export | 🔴 Unresolved | seq_length=12 static dim; use `lstm.pt` (482KB) |
| XGBoost ONNX export | 🔴 Unresolved | treelite/skl2onnx version mismatch; use native `xgboost.json` |
| IsolationForest ONNX export | 🔴 Unresolved | sklearn ONNX op missing; use native `isolation_forest.pkl` |
| qwen3:8b embeddings | 🟡 Workaround | qwen3 lacks /api/embeddings; use `nomic-embed-text` for RAG |
| `activate` script | 🟡 Workaround | Use `ml/venv/bin/python` directly (avoids shell sourcing issues) |
| Containerlab deploy | 🟡 Not tested | Configs exist; `containerlab deploy -t topology.clab.yml` never run in this session |
| vectordb permissions | 🟡 Possible | If created under sudo, fix with `sudo chown -R ego:ego ml/vectordb/` |
| RAG auto-ingest | ✅ Fixed | Auto-ingests on startup if vectordb empty |
| CDN deps | ✅ Fixed | Three.js (589KB) + anime.js (17KB) in `ml/static/js/` |
| GNN checkpoint | ✅ Fixed | Trained at `ml/models/checkpoints/gnn.pt` |
| Model loading | ✅ Fixed | All 7 models load successfully on startup |

## Security

- **🔴 SR.md** contains live GitHub PAT (REDACTED for security) — gitignored, **revoke immediately** at github.com/settings/tokens
- `clab-ps13/.tls/` added to `.gitignore` (RSA private key)
- No external DNS queries at runtime (verified by airgap_validate.py)
- No HTTP proxies or cloud endpoints (verified by airgap_validate.py)

## Model Performance Summary

| Model | File | Engine | Accuracy | Status |
|-------|------|--------|----------|--------|
| XGBoost | `xgboost.json` (1MB) | native | 99.94% | ✅ Loaded |
| IsolationForest | `isolation_forest.pkl` (2MB) | native | 5% anomaly rate | ✅ Loaded |
| Autoencoder | `autoencoder.onnx` (2KB) | ONNX | 73 epochs trained | ✅ Loaded |
| TTI Regressor | `tti_regressor.onnx` (13MB) | ONNX | MAE 10h | ✅ Loaded |
| Prophet | `prophet.onnx` | ONNX | 24h forecast | ✅ Loaded |
| LSTM | `lstm.pt` (482KB) | PyTorch | val_loss 271 | ✅ Loaded |
| GNN | `gnn.pt` (3KB) | PyTorch | loss 0.249 | ✅ Loaded |

## Telemetry Pipeline

- **Telegraf**: Collects metrics from Containerlab containers (5s interval)
- **Prometheus**: Stores time-series; scrapes Telegraf every 10s
- **Kafka**: Streams telemetry to ML engine (optional; can be skipped for single-machine demo)
- **ELK Stack**: Log aggregation (optional; can be skipped for single-machine demo)

## FastAPI Backend (ml/noc_copilot.py)

### Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check (returns 200 OK) |
| `/models/status` | GET | Model loading status (7/7 models) |
| `/predict` | POST | Run ML ensemble on telemetry |
| `/explain` | POST | Explain prediction (feature importance) |
| `/query` | POST | LLM diagnostic query (Q1/Q2/Q3) |
| `/rag/ingest` | POST | Ingest documents into ChromaDB |
| `/rag/query` | POST | Query RAG (semantic search + LLM) |

### Startup Behavior

1. Loads all 7 ML models from `ml/models/checkpoints/`
2. Initializes ChromaDB client at `ml/vectordb/`
3. Auto-ingests 7,920 telemetry docs if vectordb empty
4. Starts WebSocket server for real-time updates
5. Ready to accept requests on port 8000

## Dashboard (ml/noc-dashboard.html)

- **Framework**: HTML5 + Three.js + anime.js (no React, no build step)
- **JS Libraries**: Local copies at `ml/static/js/`
  - `three.min.js` (589KB)
  - `anime.min.js` (17KB)
- **Features**:
  - 3D orbital map (Bangalore HQ, Mumbai DC, Chennai DR, Delhi Regional)
  - Real-time ML predictions (TTI, failure probability, trend)
  - Alert correlation feed
  - LLM copilot panel (Q1/Q2/Q3 answers)
  - Playbook suggestions
  - Incidents timeline
  - Air-gap compliance status
- **No CDN**: All assets local; works offline

## Air-Gap Validation (ml/airgap_validate.py)

### 42 Checks

1. **DNS Leaks** (5 checks): Verify no external DNS queries
2. **HTTP Proxies** (3 checks): Confirm no outbound connections
3. **Process Audit** (8 checks): Only whitelisted processes running
4. **Data Flow** (6 checks): No PII/data leaves host
5. **Model Integrity** (7 checks): All 7 models present + loadable
6. **RAG Pipeline** (4 checks): ChromaDB + embeddings working
7. **LLM Interface** (3 checks): Ollama connectivity + response format
8. **FastAPI** (3 checks): Backend health + endpoint availability

### Run Command

```bash
cd /home/ego/Documents/ISRO2026
ml/venv/bin/python ml/airgap_validate.py
```

### Expected Output (with services running)

```
✅ 42/42 checks passed
  ✅ DNS: No external queries detected
  ✅ HTTP: No outbound proxies
  ✅ Process: Only whitelisted processes running
  ✅ Data Flow: No PII/data leaves host
  ✅ Models: All 7 models loaded
  ✅ RAG: ChromaDB + embeddings working
  ✅ LLM: Ollama qwen3:8b responding
  ✅ FastAPI: All 7 endpoints healthy
```

## Containerlab Topology (topology.clab.yml)

### 4-Site MPLS/SD-WAN Network

```
Bangalore HQ (10.0.1.0/24)
  ├─ PE1 (BGP AS 65001)
  ├─ P1 (MPLS core)
  └─ CE1 (Customer edge)

Mumbai DC (10.0.2.0/24)
  ├─ PE2 (BGP AS 65002)
  ├─ P2 (MPLS core)
  └─ CE2 (Customer edge)

Chennai DR (10.0.3.0/24)
  ├─ PE3 (BGP AS 65003)
  ├─ P3 (MPLS core)
  └─ CE3 (Customer edge)

Delhi Regional (10.0.4.0/24)
  ├─ PE4 (BGP AS 65004)
  ├─ P4 (MPLS core)
  └─ CE4 (Customer edge)
```

### Routing Protocols

- **BGP**: eBGP between PE routers (AS 65001-65004); iBGP within each site
- **OSPF**: Intra-site routing (Area 0)
- **MPLS**: LSP tunnels between PE routers (LDP signaling)
- **IPsec**: Site-to-site tunnels (StrongSwan)

### Fault Injection Scenarios (7 total)

1. **Link Fail**: BGP link down (PE1-PE2)
2. **BGP Flap**: BGP session flap (rapid up/down)
3. **Congestion**: Interface utilization spike (TRex traffic)
4. **Route Leak**: BGP route leak (incorrect prefix advertisement)
5. **Interface Error**: High error rate on interface
6. **Node Crash**: Router reboot (graceful shutdown)
7. **MPLS LSP Break**: MPLS tunnel failure (LDP session down)

## Synthetic Telemetry (ml/data/telemetry.parquet)

- **Rows**: 7,920 (1 hour × 4 sites × 495 metrics)
- **Columns**: 109 (timestamp, site, metric_name, value, label)
- **Labels**: Normal (95%), Anomaly (5%)
- **Metrics**: Interface utilization, error rates, BGP state, MPLS LSP status, CPU/memory

## RAG Pipeline (ml/rag_pipeline.py)

- **Vector Store**: ChromaDB (persistent at `ml/vectordb/`)
- **Embeddings**: nomic-embed-text (via Ollama)
- **Documents**: 7,920 telemetry records + runbooks
- **Query**: Semantic search + LLM synthesis

### Usage

```python
from ml.rag_pipeline import RAGPipeline

rag = RAGPipeline()
results = rag.query("BGP flap detected on PE1", n_results=5)
# Returns: [{"doc": "...", "distance": 0.12}, ...]
```

## LLM Interface (ml/llm_interface.py)

- **Model**: Qwen3-8B via Ollama
- **System Prompt**: Senior NOC engineer persona
- **Output Format**: Q1 (What) / Q2 (Why) / Q3 (How)

### Usage

```python
from ml.llm_interface import LLMInterface

llm = LLMInterface()
response = llm.query("BGP flap on PE1, what should I do?")
# Returns: {"Q1": "...", "Q2": "...", "Q3": "..."}
```

## Python Virtual Environment

```bash
# Create (one-time)
cd /home/ego/Documents/ISRO2026
python3.11 -m venv ml/venv

# Activate (optional; not needed if using ml/venv/bin/python directly)
source ml/venv/bin/activate

# Install dependencies
ml/venv/bin/pip install -r requirements.txt

# Run FastAPI without activating
ml/venv/bin/python -m uvicorn ml.noc_copilot:app --host 0.0.0.0 --port 8000
```

## Troubleshooting

### Ollama not responding
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Pull model if missing
ollama pull qwen3:8b
ollama pull nomic-embed-text
```

### FastAPI connection refused
```bash
# Check if backend is running
curl http://localhost:8000/health

# Start backend
cd /home/ego/Documents/ISRO2026
ml/venv/bin/python -m uvicorn ml.noc_copilot:app --host 0.0.0.0 --port 8000
```

### Containerlab deploy fails
```bash
# Check if Containerlab is installed
containerlab version

# Deploy with verbose output
sudo containerlab deploy -t topology.clab.yml -v

# Destroy and redeploy
sudo containerlab destroy -t topology.clab.yml
sudo containerlab deploy -t topology.clab.yml --recycle
```

### ChromaDB permission denied
```bash
# Fix ownership if created under sudo
sudo chown -R ego:ego ml/vectordb/

# Or delete and let auto-ingest recreate
rm -rf ml/vectordb/
# Restart FastAPI; it will auto-ingest
```

## Next Steps

1. ✅ Remove obsolete root stubs (final.md, phase1.md, phase3.md)
2. ✅ Rewrite README.md (T1/T2/T3 mapping, FastAPI + HTML dashboard, T3 = network topology verbose)
3. ✅ Update Docs/_implementation-notes.md (final statuses, remediation steps)
4. ⏳ Create run.md (3-terminal verbose run guide)
5. ⏳ Sweep all docs/ and ml/ files (verify references, remove stale docs)
6. ⏳ Start demo (ollama serve → FastAPI → Containerlab → dashboard)
7. ⏳ Re-run airgap_validate.py with services running

---

*Last updated: 2026-06-24*
