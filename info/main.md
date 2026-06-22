# Main Architecture — PS13

## Air-Gapped Predictive Copilot for Secure MPLS Operations

An AI-powered NOC copilot that simulates a multi-site enterprise MPLS/SD-WAN network, streams real-time telemetry through a Prometheus/Kafka pipeline, predicts network failures using an ensemble of 7 ML models, and provides natural-language diagnostic assistance via an offline LLM with RAG over 50+ internal runbook documents — all running air-gapped on a single RTX 4060 laptop.

---

## Topology (Containerlab — 4 Sites)

```
┌─────────────────────────────────────────────────────────────────────┐
│                       BGP/OSPF/MPLS Backbone                        │
│                                                                     │
│    ┌─────────┐         ┌─────────┐         ┌─────────┐             │
│    │ P1 (P)  │◄───────►│ P2 (P)  │◄───────►│ P3 (P)  │             │
│    │  Core   │  eBGP   │  Core   │  eBGP   │  Core   │             │
│    └────┬────┘         └────┬────┘         └────┬────┘             │
│          │                  │                  │                    │
│    ┌─────┴─────┐    ┌──────┴──────┐    ┌──────┴──────┐             │
│    │ PE1 (PE)  │    │ PE2 (PE)    │    │ PE3 (PE)    │             │
│    │ Bangalore │    │ Mumbai      │    │ Chennai     │             │
│    │ HQ        │    │ DC          │    │ DR          │             │
│    └─────┬─────┘    └──────┬──────┘    └──────┬──────┘             │
│          │                 │                   │                    │
│    ┌─────┴─────┐    ┌──────┴──────┐    ┌──────┴──────┐             │
│    │ CE1 (CE)  │    │ CE2 (CE)    │    │ CE3 (CE)    │             │
│    │ Campus    │    │ DC Servers  │    │ DR Servers  │             │
│    └───────────┘    └─────────────┘    └─────────────┘             │
│                                                                     │
│    ┌──────────────────────────────────────────────────────┐        │
│    │           IPsec Tunnel (Bangalore ↔ Delhi)           │        │
│    │    ┌─────────────────┐      ┌─────────────────┐      │        │
│    │    │ IPsec GW Bengal │◄────►│ IPsec GW Delhi  │      │        │
│    │    └─────────────────┘      └─────────────────┘      │        │
│    └──────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────┘
```

### Device Roles
- **P Routers**: Core MPLS backbone, LDP + BGP-free core, high-speed label switching
- **PE Routers**: MPLS edge, BGP/OSPF route exchange, LSP ingress/egress, VRF segmentation
- **CE Routers**: Customer edge, single-homed or dual-homed to PE, standard IP routing
- **IPsec Gateways**: Site-to-site encrypted overlay across untrusted transport

### Fault Scenarios (7)
1. **Link Failure**: Interface down on core link between P1-P2
2. **BGP Flap**: PE2 BGP session to PE1 oscillates (hold timer / update delay)
3. **Congestion**: Link utilization crosses 90% threshold (TRex burst)
4. **Route Leak**: CE2 accidentally advertises DC prefixes to wrong VRF
5. **Interface Errors**: CRC errors escalating on P3-PE3 link
6. **Node Crash**: P2 container crash (simulated hard failure)
7. **LSP Break**: MPLS label path breaks between PE1→PE3 (label withdrawal)

---

## Data Pipeline

```
┌────────────────┐    ┌────────────┐    ┌──────────────┐    ┌────────────┐
│ Containerlab   │    │ Telegraf   │    │  Prometheus  │    │   Kafka    │
│ FRR Nodes      │───►│ Agents     │───►│  TSDB +      │───►│  Stream    │
│ (metrics 5s)   │    │ (per node) │    │  Alert Rules │    │  Broker    │
└────────────────┘    └────────────┘    └──────────────┘    └─────┬──────┘
                                                                   │
                    ┌──────────────────────────────────────────────┘
                    ▼
          ┌─────────────────────┐     ┌────────────────────────┐
          │   ML Engine         │     │   LLM Copilot          │
          │   ┌─────────────┐   │     │   ┌─────────────────┐  │
          │   │ LSTM        │   │     │   │ Ollama Qwen3-8B │  │
          │   │ (time-series)│   │     │   └────────┬────────┘  │
          │   ├─────────────┤   │     │            │            │
          │   │ Prophet     │   │     │   ┌────────▼────────┐  │
          │   │ (trend/sea) │   │     │   │ ChromaDB RAG    │  │
          │   ├─────────────┤   │     │   │ (50+ runbooks)  │  │
          │   │ GNN (graph) │   │     │   └─────────────────┘  │
          │   ├─────────────┤   │     └────────────────────────┘
          │   │ XGBoost     │   │
          │   │ (classifier)│   │     ┌────────────────────────┐
          │   ├─────────────┤   │     │   NOC Workflow         │
          │   │ IsoForest   │   │     │   ┌─────────────────┐  │
          │   │ (anomaly)   │   │     │   │ NetworkX Graph  │  │
          │   ├─────────────┤   │     │   │ Alert Correlate │  │
          │   │ Autoencoder │   │     │   ├─────────────────┤  │
          │   │ (recon err) │   │     │   │ Playbook Suggest│  │
          │   ├─────────────┤   │     │   ├─────────────────┤  │
          │   │ TTI Regr.   │   │     │   │ Incident Summ.  │  │
          │   │ (time-to-   │   │     │   └─────────────────┘  │
          │   │  incident)  │   │     └────────────────────────┘
          │   └─────────────┘   │
          └─────────────────────┘
```

---

## Terminal Breakdown

### Terminal 1 (port 5173) — Network Topology UI
- **Framework**: React 18 + Vite + Three.js + R3F + @react-three/drei
- **State**: Zustand (simulation state, router selections, fault injection params)
- **3D Scene**: 4-site MPLS network with router meshes, animated link lines, BGP peer indicators
- **Interactions**: Click router → info panel (hostname, model, BGP peers, link states, MPLS labels)
- **Fault Injection Panel**: Slide-toggle for each of 7 fault scenarios, reset button
- **Animations**: Anime.js for traffic flow particles, alert flash effects, BGP session status transitions
- **Data Flow**: REST GET /api/simulation/state for initial load, WS /ws/topology for live updates

### Terminal 2 (port 8000) — Backend
- **Simulation Orchestrator**: Containerlab lifecycle (start/stop/reset), FRR config generator per router
- **Telemetry Pipeline Bridge**: Consumes Telegraf → Prometheus metrics, forwards to Kafka topics
- **ML Inference Engine**: 7 models loaded on-demand; batch inference on Prometheus data, event-driven inference on Kafka stream
- **LLM Copilot**: Ollama API calls to Qwen3-8B with RAG context from ChromaDB; Qwen3-4B-Thinking for lightweight fallback
- **Air-Gap Scanner**: Periodic DNS, HTTP, process, and data-flow checks; reports compliance score
- **API Endpoints**:
  - `GET /api/simulation/state` — Current topology + fault status
  - `POST /api/simulation/fault` — Inject fault scenario
  - `POST /api/simulation/reset` — Reset to healthy state
  - `GET /api/telemetry/metrics` — Prometheus metrics snapshot
  - `GET /api/ml/predictions` — Latest model predictions
  - `POST /api/ml/query` — Ad-hoc ML inference on custom metrics
  - `POST /api/copilot/query` — Ask LLM with structured output
  - `GET /api/copilot/context` — Available RAG context sources
  - `GET /api/workflow/alerts` — Correlated alerts
  - `POST /api/workflow/playbook` — Suggest playbook for incident
  - `GET /api/airgap/status` — Air-gap compliance check
  - `WS /ws/topology` — Live topology state updates
  - `WS /ws/ml` — Live ML prediction stream
  - `WS /ws/alerts` — Live alert stream

### Terminal 3 (port 5174) — Analytics Dashboard
- **Framework**: React 18 + Vite + anime.js + ECharts
- **State**: Zustand (predictions, alerts, copilot responses, airgap status)
- **Panels**:
  1. **ML Prediction Panel**: TTI countdown, failure probability gauges, trend charts (ECharts)
  2. **Alert Correlation Feed**: Topology-aware grouped alerts with blast radius overlay
  3. **LLM Copilot Panel**: Chat interface with Q1/Q2/Q3 structured answer rendering
  4. **Playbook Suggestion Panel**: Ranked playbooks for active incidents
  5. **Incidents Timeline**: Severity progression, resolved vs active counters
  6. **Air-Gap Compliance**: Green/amber/red status with per-check detail
- **Data Flow**: WS push from backend for all live data; REST for historical queries

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Containerlab for simulation | Standard for container-based NOS simulation; FRR images available; no hardware needed |
| Ensemble ML (7 models) | Each model captures different signal; combined predictions more robust than single model |
| ChromaDB RAG over runbooks | Lightweight, local, no cloud dependency; supports semantic search over internal docs |
| Qwen3-8B primary LLM | Runs on RTX 4060 (8GB VRAM); strong reasoning for network diagnostics |
| Qwen3-4B-Thinking fallback | Uses fewer resources; good for rapid/lightweight queries |
| NetworkX for alert correlation | Lightweight graph analysis; no external graph DB needed |
| 3-terminal architecture | Separates concerns: visualization, computation, analytics; independent scaling |
| No cloud dependency | True air-gap; all infra via Docker + floci.io local emulation |
| FastAPI + WebSocket | Async-first; ideal for streaming telemetry and real-time ML predictions |
| Zustand for state | Lightweight, no boilerplate; works for both frontends |

---

## Infrastructure

| Service | Role | Technology |
|---------|------|-----------|
| floci.io S3 | Runbook + model storage | Local S3-compatible |
| floci.io DynamoDB | Incident history, alert state | Local DynamoDB-compatible |
| floci.io Lambda | Alert processor (lightweight) | Local Lambda emulation |
| Docker | Simulation containers, pipeline services | docker-compose |
| Ollama | LLM runtime | Local GPU-accelerated |
| ChromaDB | Vector store for RAG | Local persistent |

---

## Hardware Target

| Component | Spec |
|-----------|------|
| GPU | NVIDIA RTX 4060 (8GB VRAM) |
| CPU | AMD Ryzen 9 8945HS (8 cores / 16 threads) |
| RAM | 15 GB DDR5 |
| Storage | Local NVMe SSD |
| OS | Linux (Ubuntu 24.04) |

---

*Air-gapped by design. No cloud dependency. All data stays local.*
