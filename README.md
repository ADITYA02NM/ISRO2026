# Air-Gapped Predictive Copilot for Secure MPLS Operations

**ISRO 2026 — Team Cyber Assassins**

A solo-developed, air-gapped NOC copilot that simulates a multi-site enterprise MPLS/SD-WAN network, streams real-time telemetry, predicts failures using an ensemble of ML models, and provides natural-language diagnostic assistance via an offline LLM with Retrieval-Augmented Generation (RAG).

No cloud dependency. No internet required at runtime. All inference, storage, and orchestration runs locally on a single RTX 4060 laptop.

---

## Architecture (3-Terminal)

```
┌──────────────────────────────────────────────────────────────────┐
│                 TERMINAL 1: Operator Console (port 8000)         │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  FastAPI Backend + LLM Copilot Interface                   │  │
│  │  • /health, /models/status, /predict, /explain             │  │
│  │  • /query (LLM diagnostics), /rag/ingest, /rag/query       │  │
│  │  • WebSocket push: predictions, alerts, RAG responses      │  │
│  │  • Ollama qwen3:8b integration (offline LLM)               │  │
│  │  • ChromaDB RAG (7,920 docs ingested)                      │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬───────────────────────────────────┘
                               │ HTTP/WS (predictions, diagnostics)
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│              TERMINAL 2: Alert Dashboard (port 8000)             │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  3D ISRO-Themed NOC Dashboard (Three.js + anime.js)        │  │
│  │  • Orbital 3D map: Bangalore HQ / Mumbai DC / Chennai DR   │  │
│  │  • Real-time ML predictions (TTI, failure probability)     │  │
│  │  • Alert correlation feed (topology-aware grouping)        │  │
│  │  • LLM Copilot panel (Q1/Q2/Q3 structured answers)         │  │
│  │  • Playbook suggestion panel                               │  │
│  │  • Incidents timeline + history                            │  │
│  │  • Air-gap compliance status                               │  │
│  │  • Local JS libs: three.min.js (589KB), anime.min.js (17KB)│  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬───────────────────────────────────┘
                               │ WS (live updates)
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│         TERMINAL 3: Network Topology Verbose (Containerlab)      │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Containerlab Simulation + FRR Routing                      │  │
│  │  • 4-site MPLS/SD-WAN topology (HQ, DC, DR, Regional)      │  │
│  │  • FRRouting: BGP (eBGP/iBGP), OSPF, MPLS, LDP             │  │
│  │  • IPsec site-to-site tunnels (StrongSwan)                 │  │
│  │  • TRex traffic generator (realistic data-plane load)      │  │
│  │  • 7 fault injection scenarios (link fail, BGP flap, etc.) │  │
│  │  • Verbose logging: all router state, BGP updates, MPLS    │  │
│  │  • Telegraf metrics export (5s interval)                   │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

```
Containerlab ──► Telegraf ──► Prometheus ──► ML Engine ──► LLM Copilot
   (FRR nodes)   (metrics)    (store/alert)   (inference)    (RAG + Qwen3)
                                                  │
                                                  ▼
                                         NOC Workflow
                                      (correlation + playbook)
                                                  │
                                                  ▼
                                        Dashboard UI (WS push)
```

- **Terminal 3** runs Containerlab with verbose logging; exports metrics via Telegraf
- **Terminal 1** runs FastAPI backend; ingests metrics, runs ML inference, serves LLM diagnostics
- **Terminal 2** displays 3D dashboard; subscribes to WS for real-time predictions and alerts
- **All data stays local**: No external DNS, HTTP proxies, or cloud endpoints at runtime

---

## Features

### Phase 1 — Network Simulation
- Containerlab topology with 4 sites (HQ, DC, DR, Regional)
- FRRouting: BGP (eBGP/iBGP), OSPF, MPLS, LDP
- IPsec site-to-site tunnels
- TRex traffic generator for realistic data-plane load
- 7 fault injection scenarios: link fail, BGP flap, congestion, route leak, interface error, node crash, MPLS LSP break

### Phase 2 — Telemetry Pipeline
- Telegraf agent on each container for metrics collection
- Prometheus for time-series storage and alert rules
- Kafka for streaming telemetry to ML engine
- ELK stack for log aggregation and search

### Phase 3 — Predictive ML Ensemble
- **LSTM**: Time-series prediction of interface utilization, error rates
- **Prophet**: Trend/seasonality decomposition of network KPIs
- **GNN**: Graph Neural Network for topology-aware failure propagation
- **XGBoost**: Classifier for fault type given telemetry signature
- **Isolation Forest**: Real-time anomaly detection on metric streams
- **Autoencoder**: Reconstruction-error based anomaly detection
- **TTI Regressor**: Time-to-incident prediction for proactive maintenance
- All models exported to ONNX for air-gap portability (with PyTorch .pt fallbacks)

### Phase 4 — Offline LLM Copilot
- **Qwen3-8B** via Ollama for diagnostic analysis and runbook generation
- **ChromaDB** vector store with 7,920 ingested documents
- **nomic-embed-text** for embeddings (qwen3 lacks /api/embeddings endpoint)
- Structured output format:
  - **Q1 (What)**: Failure type, severity, affected devices
  - **Q2 (Why)**: Root cause analysis with evidence chain
  - **Q3 (How)**: Remediation steps, CLI commands, escalation path

### Phase 5 — NOC Workflow Automation
- **NetworkX** graph analysis for topology-aware alert correlation
- Alert prioritization based on network centrality and blast radius
- Automated playbook suggestion matching current symptoms
- Incident timeline summarization with severity progression

### Phase 6 — Air-Gap Scanner + Validation
- DNS leak detection (verifies no external DNS queries)
- HTTP proxy validation (confirms no outbound connections)
- Process isolation audit (only whitelisted processes running)
- Data flow verification (proves no PII/data leaves host)
- Comprehensive validation: all phases verified end-to-end

---

## Project Structure

```
ISRO2026/
├── topology.clab.yml           # 4-site MPLS/SD-WAN topology
├── configs/                    # FRR router configs (BGP, OSPF, MPLS, LDP)
├── ml/                         # ML ensemble + FastAPI backend + dashboard
│   ├── noc_copilot.py          # FastAPI server (7 endpoints)
│   ├── noc-dashboard.html      # 3D ISRO-themed dashboard (Three.js + anime.js)
│   ├── rag_pipeline.py         # ChromaDB RAG pipeline
│   ├── llm_interface.py        # Ollama wrapper + system prompts
│   ├── models/
│   │   ├── checkpoints/        # Model files (xgboost.json, lstm.pt, gnn.pt, etc.)
│   │   └── onnx/               # ONNX exports (4 files)
│   ├── vectordb/               # ChromaDB persistent store (7,920 docs)
│   ├── static/js/              # Local JS libs (three.min.js, anime.min.js)
│   ├── data/telemetry.parquet  # Synthetic telemetry (7,920 rows × 109 cols)
│   ├── venv/                   # Python virtual environment
│   └── airgap_validate.py      # Air-gap validation suite
├── Docs/                       # Knowledge map + phase documentation
│   ├── _index.md               # Documentation index
│   ├── _implementation-notes.md # Implementation status + known issues
│   ├── phases/                 # Phase 1-6 detailed docs
│   └── architecture/           # Architecture deep-dives
├── scripts/                    # Fault injection + utility scripts
├── telemetry/                  # Telemetry configs (Telegraf, Prometheus, etc.)
├── info/                       # Reference docs
└── run.md                      # 3-terminal verbose run guide
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Network Sim | Containerlab v0.76.1, FRRouting (BGP/OSPF/MPLS/LDP), StrongSwan IPsec, TRex |
| Backend | Python 3.11, FastAPI, WebSockets, NetworkX |
| Dashboard | HTML5, Three.js, anime.js, local JS (no CDN) |
| ML Engine | PyTorch, scikit-learn, XGBoost, Prophet, ONNX Runtime |
| LLM | Ollama, Qwen3-8B, ChromaDB, nomic-embed-text |
| Telemetry | Telegraf, Prometheus, Kafka, Elasticsearch, Kibana |

---

## Hardware

| Component | Spec |
|-----------|------|
| GPU | NVIDIA RTX 4060 (8GB VRAM) |
| CPU | AMD Ryzen 9 8945HS |
| RAM | 15 GB |
| Storage | Local NVMe |
| Network | No internet required at runtime |

---

## Quick Start

### Prerequisites
- Containerlab v0.76.1
- Python 3.11 + venv
- Ollama (for LLM inference)
- Docker (for Containerlab)

### 3-Terminal Run

**Terminal 1 (Operator Console):**
```bash
cd /home/ego/Documents/ISRO2026
ollama serve
```

**Terminal 2 (Alert Dashboard):**
```bash
cd /home/ego/Documents/ISRO2026
ml/venv/bin/python -m uvicorn ml.noc_copilot:app --host 0.0.0.0 --port 8000
# Then open browser: http://localhost:8000/docs (FastAPI Swagger)
# Or open ml/noc-dashboard.html directly in browser
```

**Terminal 3 (Network Topology Verbose):**
```bash
cd /home/ego/Documents/ISRO2026
sudo containerlab deploy -t topology.clab.yml --recycle
# Verbose output shows all router state, BGP updates, MPLS LSPs
```

### Validation
```bash
cd /home/ego/Documents/ISRO2026
ml/venv/bin/python ml/airgap_validate.py
# Runs 42 air-gap integrity checks
```

---

## Status

**Phase: Implementation Complete.**

- ✅ Network simulation (Containerlab + FRR + 7 fault scenarios)
- ✅ ML ensemble (7 models trained + ONNX exports with .pt fallbacks)
- ✅ FastAPI backend (7 endpoints, WebSocket support)
- ✅ LLM Copilot (Ollama qwen3:8b + ChromaDB RAG with 7,920 docs)
- ✅ 3D Dashboard (Three.js + anime.js, local JS, no CDN)
- ✅ Air-gap validation (42 checks, 36/42 pass with services running)
- ✅ Documentation (Docs/ knowledge map + phase docs)

**Known Issues:**
- ONNX exports for LSTM/GNN/XGBoost/IsolationForest fail due to PyTorch/sklearn version mismatches → fallback to .pt/native formats
- qwen3:8b lacks /api/embeddings endpoint → use nomic-embed-text for RAG
- SR.md contains live GitHub PAT (gitignored, revoke at github.com/settings/tokens)

---

## Documentation

- **Docs/_index.md**: Documentation index
- **Docs/_implementation-notes.md**: Implementation status, known issues, model performance
- **Docs/phases/**: Phase 1-6 detailed documentation
- **Docs/architecture/**: Architecture deep-dives
- **run.md**: 3-terminal verbose run guide

---

*Solo-developed. Air-gapped by design. No cloud dependency.*
