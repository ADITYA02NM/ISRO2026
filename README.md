# Air-Gapped Predictive Copilot for Secure MPLS Operations

**ISRO 2026 — Team Cyber Assassins**

A solo-developed, air-gapped NOC copilot that simulates a multi-site enterprise MPLS/SD-WAN network, streams real-time telemetry, predicts failures using an ensemble of ML models, and provides natural-language diagnostic assistance via an offline LLM with Retrieval-Augmented Generation (RAG).

No cloud dependency. No internet required at runtime. All inference, storage, and orchestration runs locally on a single RTX 4060 laptop.

---

## Architecture (3-Terminal)

```
┌──────────────────────────────────────────────────────────────────┐
│                    TERMINAL 1: Network Topology (port 5173)      │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  3D Multi-site MPLS Network (R3F + drei + Three.js)        │  │
│  │  • Bangalore HQ / Mumbai DC / Chennai DR / Delhi Regional  │  │
│  │  • PE/P/CE routers + IPsec gateways + SD-WAN edges         │  │
│  │  • BGP peer links, MPLS LSPs, traffic utilization          │  │
│  │  • Click router → hover info (model, peers, status)        │  │
│  │  • Fault injection panel (link fail, BGP flap, congestion) │  │
│  │  • Anime.js animated traffic + alert indicators            │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬───────────────────────────────────┘
                               │ REST (sim control, config push)
                               │ WS (live topology updates)
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                    TERMINAL 2: Backend (port 8000)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ Containerlab  │  │ Telemetry    │  │ ML Engine            │   │
│  │ Orchestrator  │→│ Pipeline     │→│ • LSTM (time series)  │   │
│  │ • FRR BGP/    │  │ • Telegraf   │  │ • Prophet (trend)    │   │
│  │   OSPF/MPLS   │  │ • Prometheus │  │ • GNN (topology)     │   │
│  │ • IPsec       │  │ • Kafka      │  │ • XGBoost (classify) │   │
│  │ • TRex traffic│  │ • ELK Stack  │  │ • IsolationForest    │   │
│  │ • 7 fault     │  │              │  │ • Autoencoder        │   │
│  │   scenarios   │  │              │  │ • TTI regressor      │   │
│  └──────────────┘  └──────────────┘  └──────────┬───────────┘   │
│                                                  │              │
│  ┌──────────────────────┐  ┌──────────────────┐  │              │
│  │ LLM Copilot          │  │ NOC Workflow     │  │              │
│  │ • Qwen3-8B (Ollama)  │  │ • NetworkX graph │  │              │
│  │ • ChromaDB RAG       │  │ • Alert corr.    │  │              │
│  │ • Qwen3-4B-Thinking  │  │ • Playbook gen.  │  │              │
│  │   (fallback)         │  │ • Incident sum.  │  │              │
│  └──────────────────────┘  └──────────────────┘  │              │
│                                                   │              │
│  ┌──────────────────────────────────────────┐     │              │
│  │ Air-Gap Integrity Scanner                │     │              │
│  │ • DNS leak detection  • Process audit    │     │              │
│  │ • HTTP proxy check    • Data flow verify │     │              │
│  └──────────────────────────────────────────┘     │              │
└──────────────────────────────┬───────────────────────────────────┘
                               │ WS (predictions, alerts, RAG)
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                    TERMINAL 3: Analytics Dashboard (port 5174)   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Network Analytics Dashboard (React + anime.js + ECharts)  │  │
│  │  • ML Prediction Panel (TTI, failure probability, trend)   │  │
│  │  • Alert Correlation Feed (topology-aware grouping)        │  │
│  │  • LLM Copilot Panel (Q1/Q2/Q3 structured answers)        │  │
│  │  • Playbook Suggestion Panel                              │  │
│  │  • Incidents Timeline + History                           │  │
│  │  • Air-Gap Compliance Status                             │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

```
Containerlab ──► Telegraf ──► Prometheus ──► Kafka ──► ML Engine ──► LLM Copilot
   (FRR nodes)   (metrics)    (store/alert)   (stream)   (inference)    (RAG + Qwen3)
                                                              │
                                                              ▼
                                                     NOC Workflow
                                                  (correlation + playbook)
                                                              │
                                                              ▼
                                                    Dashboard UI (WS push)
                                                 + Topology UI (REST poll)
```

- **Topology View** polls REST for simulation state, subscribes to WS for real-time topology updates
- **Dashboard** subscribes to WS push from ML predictions, alert correlation, and copilot responses
- **Simulation → Telemetry**: Containerlab exports interface counters, BGP state, CPU/memory every 5s
- **Telemetry → ML**: Prometheus stores, Kafka streams, ML engine runs periodic + event-driven inference
- **ML → LLM**: Prediction anomalies trigger LLM diagnostic analysis with runbook RAG context
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
- All models exported to ONNX for air-gap portability

### Phase 4 — Offline LLM Copilot
- **Qwen3-8B** via Ollama for diagnostic analysis and runbook generation
- **ChromaDB** vector store with 50+ internal runbook documents
- **Qwen3-4B-Thinking** as lightweight fallback for resource-constrained queries
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
├── devices-ui/             # Terminal 1: Network Topology UI (Vite + R3F)
├── dashboard/              # Terminal 3: Analytics Dashboard (Vite + React)
├── backend/                # Terminal 2: FastAPI backend
├── simulation/             # Containerlab topology definitions
│   ├── topology.clab.yml   # 4-site MPLS topology
│   ├── frr/                # FRRouting configs (BGP, OSPF, MPLS, LDP)
│   ├── ipsec/              # StrongSwan IPsec configurations
│   └── scripts/            # Fault injection automation
├── telemetry/              # Pipeline configurations
│   ├── telegraf/           # Telegraf agent configs
│   ├── prometheus/         # Prometheus scrape + alert rules
│   ├── kafka/              # Kafka topic definitions
│   └── elasticsearch/      # ELK stack configs
├── ml/                     # Predictive models
│   ├── lstm/               # Time-series prediction
│   ├── prophet/            # Trend decomposition
│   ├── gnn/                # Graph neural network
│   ├── xgboost/            # Fault classification
│   ├── anomaly/            # Isolation Forest + Autoencoder
│   └── tti/                # Time-to-incident regressor
├── llm/                    # LLM Copilot
│   ├── chroma/             # ChromaDB vector store
│   ├── rag/                # RAG pipeline code
│   └── runbooks/           # Internal runbook documents (50+)
├── airgap/                 # Air-gap integrity scanner
└── info/                   # Documentation
    ├── main.md             # Architecture deep-dive
    ├── frontend.md          # UI component trees
    ├── flow.md             # Data flow sequences
    ├── build.md            # Build plan (6 phases)
    ├── resources.md         # Stack references
    └── learn.md            # Learning path
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Network Sim | Containerlab, FRRouting (BGP/OSPF/MPLS/LDP), StrongSwan IPsec, TRex |
| Frontend (T1) | React 18, Vite, Three.js, R3F, @react-three/drei, Zustand |
| Frontend (T3) | React 18, Vite, anime.js, ECharts, Zustand |
| Backend | Python 3.11, FastAPI, WebSockets, NetworkX |
| ML Engine | PyTorch, scikit-learn, XGBoost, Prophet, ONNX Runtime |
| LLM | Ollama, Qwen3-8B, Qwen3-4B-Thinking, ChromaDB, LangChain |
| Telemetry | Telegraf, Prometheus, Kafka, Elasticsearch, Kibana |
| Infrastructure | floci.io (local S3/DynamoDB/Lambda emulation), Docker |

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

## Build Roadmap (6 Phases)

| Phase | Focus | Duration |
|-------|-------|----------|
| 1 | Containerlab Network Simulation (topology, FRR, IPsec, TRex, 7 fault scenarios) | Days 1-3 |
| 2 | Telemetry Pipeline (Telegraf → Prometheus → Kafka → ELK) | Days 3-5 |
| 3 | Predictive ML Ensemble (6 models + TTI regressor + ONNX export) | Days 5-8 |
| 4 | Offline LLM Copilot (Qwen3-8B, ChromaDB RAG, structured Q1/Q2/Q3) | Days 8-10 |
| 5 | NOC Workflow Automation (alert correlation, playbook generation, summaries) | Days 10-12 |
| 6 | Air-Gap Scanner + End-to-End Validation | Days 12-14 |

Each phase includes dual-frontend integration points. Phase 1 can run standalone; Phases 2-6 build on it incrementally.

---

## Status

**Phase: Architecture complete.** All 8 documentation files rewritten for PS13 alignment. Implementation begins after PS13 submission review.

---

*Solo-developed. Air-gapped by design. No cloud dependency.*

