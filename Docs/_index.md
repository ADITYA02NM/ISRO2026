---
created: 2026-06-23
tags: [ps13, index, knowledge-map, root]
---

# 🗺️ PS13 Knowledge Map — MPLS SD-WAN + ML NOC Copilot

**Project**: 4-site MPLS SD-WAN (Containerlab) + 7-ML ensemble + Offline LLM/RAG + 3D Dashboard
**Hardware**: Ryzen 9 8945HS + RTX 4060 (8GB) + 15GB RAM | **OS**: Arch Linux (air-gapped)

## 📂 Project Structure

```
ISRO2026/
├── topology.clab.yml       — Containerlab topology (11 nodes, 4 sites)
├── configs/                — FRRouting configs (CE/PE/P per site)
├── scripts/                — 7 fault injection scripts
├── ml/                     — All ML + server code
│   ├── noc_copilot.py      — FastAPI server (7 endpoints)
│   ├── noc-dashboard.html  — 3D ISRO dashboard (Three.js + anime.js)
│   ├── ensemble_predictor.py — Unified 7-model inference engine
│   ├── rag_pipeline.py     — ChromaDB RAG (7,920 docs)
│   ├── llm_interface.py    — Ollama client (qwen3:8b)
│   ├── airgap_validate.py  — 44-check validation suite
│   ├── venv/               — Python virtual environment
│   ├── vectordb/           — ChromaDB persistent store
│   ├── static/js/          — Local Three.js + anime.js
│   ├── data/               — telemetry.parquet (7,920×109)
│   └── models/             — 7 model files + checkpoints + ONNX exports
├── telemetry/              — Docker Compose stack configs
├── Docs/                   — 📍 YOU ARE HERE (knowledge map)
├── info/                   — 15 reference notes
├── .gitignore
└── README.md
```

## 🔗 Knowledge Graph

### 📡 Phases

| Phase | Status | Doc |
|-------|--------|-----|
| [[phases/phase-01-network-simulation\|Phase 1: Network Simulation]] | 🟡 Configs ready | FRR + Containerlab topology |
| [[phases/phase-02-telemetry-pipeline\|Phase 2: Telemetry Pipeline]] | 🟡 Configs ready | Kafka/Prometheus/ELK stack |
| [[phases/phase-03-ml-ensemble\|Phase 3: ML Ensemble]] | **✅ DONE** | 7/7 models, 3 ONNX |
| [[phases/phase-04-offline-llm-rag\|Phase 4: Offline LLM + RAG]] | **✅ DONE** | Ollama + ChromaDB |
| [[phases/phase-05-copilot-integration\|Phase 5: Copilot Integration]] | **✅ DONE** | FastAPI + dashboard |
| [[phases/phase-06-airgap-validation\|Phase 6: Air-Gap]] | **✅ DONE** | 36/42 checks pass |

### 🏗️ Architecture Docs

| Doc | Covers |
|-----|--------|
| [[architecture/network-topology\|Network Topology]] | 4 sites, MPLS, BGP, OSPF, IPsec |
| [[architecture/ml-pipeline\|ML Pipeline]] | Data flow, 109 features, model loading |
| [[architecture/server-architecture\|Server Architecture]] | Component diagram, request lifecycle |

### ⚙️ Components

| Component | File | Role |
|-----------|------|------|
| [[components/ensemble-predictor\|Ensemble Predictor]] | `ml/ensemble_predictor.py` | Core ML engine (~1400 lines) |
| [[components/noc-copilot\|NOC Copilot]] | `ml/noc_copilot.py` | FastAPI server (531 lines) |
| [[components/rag-pipeline\|RAG Pipeline]] | `ml/rag_pipeline.py` | ChromaDB vector search (330 lines) |
| [[components/llm-interface\|LLM Interface]] | `ml/llm_interface.py` | Ollama client (260 lines) |
| [[components/noc-dashboard\|NOC Dashboard]] | `ml/noc-dashboard.html` | 3D space-themed UI (~1700 lines) |

### 🧠 ML Models

| Model | Engine | Metric | Doc |
|-------|--------|--------|-----|
| XGBoost | native | 99.94% acc | [[components/models/xgboost-model\|XGBoost]] |
| Isolation Forest | native | 5.0% anomaly | [[components/models/isolation-forest-model\|Isolation Forest]] |
| TTI Regressor | ONNX | MAE 10.04h | [[components/models/tti-regressor-model\|TTI Regressor]] |
| Autoencoder | ONNX | 73 epochs | [[components/models/autoencoder-model\|Autoencoder]] |
| LSTM | torch | val_loss 271 | [[components/models/lstm-model\|LSTM]] |
| GNN | torch | 10-node graph | [[components/models/gnn-model\|GNN]] |
| Prophet | ONNX | 24h forecast | [[components/models/prophet-model\|Prophet]] |

### 🌐 Topology

| Doc | Covers |
|-----|--------|
| [[topology/sites\|Sites]] | BLR, MUM, CHE, DEL — 4-city map |
| [[topology/device-roles\|Device Roles]] | CE, PE, P — 11 FRR nodes |
| [[topology/protocols\|Protocols]] | BGP, OSPF, MPLS LDP, IPsec |
| [[topology/fault-scripts\|Fault Scripts]] | 7 fault injection scripts |
| [[data/fault-scenarios\|Fault Scenarios]] | 7 fault types + dashboard triggers |

### 📊 Data

| Doc | Covers |
|-----|--------|
| [[data/telemetry-schema\|Telemetry Schema]] | 109 features, parquet file |
| [[data/fault-scenarios\|Fault Scenarios]] | 7 fault types with patterns |

### 🚀 Deployment

| Doc | Covers |
|-----|--------|
| [[deployment/server-startup\|Server Startup]] | 3-terminal launch guide |
| [[deployment/containerlab\|Containerlab]] | Network simulation deploy |
| [[deployment/telemetry-stack\|Telemetry Stack]] | Docker Compose stack |
| [[deployment/air-gap-validation\|Air-Gap Validation]] | Offline test suite |

### 📖 Glossary

| Doc | Covers |
|-----|--------|
| [[glossary/_glossary\|Glossary]] | All terms defined |

### 📝 Reference

15 reference notes in `info/` covering: T1/T2/T3 architectures, problem statement, build notes, flow diagrams, frontend references, future plans, learning resources, and the `random.md` inspiration file for the dashboard design.

> **Project root**: `/home/ego/Documents/ISRO2026`
> **Status**: [[_implementation-notes|Implementation Notes]]
