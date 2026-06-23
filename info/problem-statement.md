# Problem Statement — PS13

## Air-Gapped Predictive Copilot for Secure MPLS Operations

---

## 1. Context & Motivation

Enterprise and ISP networks running MPLS/SD-WAN face a critical operational gap: **NOC teams react to failures rather than predicting them.** By the time an alert fires, end-users have already experienced degradation. Meanwhile, network operations are increasingly expected to run in **air-gapped environments** (defense, critical infrastructure, classified government networks) where cloud-based AI/ML tools are forbidden.

**PS13** bridges this gap by building a complete, offline, AI-powered NOC copilot that runs on a single RTX 4060 laptop — no cloud, no internet, no external dependencies. It simulates a multi-site enterprise MPLS/SD-WAN network, streams telemetry through a real-time pipeline, predicts failures using an ensemble of 7 ML models, and provides natural-language diagnostic assistance via an offline LLM (Ollama + Qwen3) with RAG over 50+ internal runbook documents.

---

## 2. Problem Statement

> **"Design and build an air-gapped predictive copilot for secure MPLS/SD-WAN operations that simulates a multi-site enterprise network, detects and predicts network anomalies using machine learning, diagnoses issues with an offline LLM + RAG pipeline, and automates NOC workflows — all running locally on a single laptop with zero cloud dependency."**

---

## 3. North Star Questions (Q1 / Q2 / Q3)

The project is evaluated against three north-star questions:

### Q1 — Network Simulation
> *"Does the simulated network behave like a real enterprise MPLS/SD-WAN?"*

**Success criteria:**
- Containerlab topology with 4 sites (Bangalore, Mumbai, Chennai, Delhi) running FRRouting
- BGP/OSPF/MPLS/LDP fully operational across all routers
- IPsec site-to-site tunnel between Bangalore and Delhi
- TRex traffic generator producing realistic data-plane load (>100K pps)
- 7 fault scenarios injectable and revertable on demand
- All state reported in real-time via WebSocket

**Weight: 35%**

### Q2 — ML Prediction & LLM Copilot
> *"Can the system predict failures before they happen and explain them in plain language?"*

**Success criteria:**
- 7-model ML ensemble (LSTM, Prophet, GNN, XGBoost, Isolation Forest, Autoencoder, TTI Regressor) running inference on telemetry stream
- Batch inference every 30s, event-driven inference < 2s
- Structured Q1/Q2/Q3 answers from LLM (What happened, Why, How to fix)
- RAG precision@5 > 0.8 over 50+ runbook documents
- Auto-trigger on prediction confidence > 0.8

**Weight: 35%**

### Q3 — Air-Gap & Automation
> *"Does everything work without touching the internet, and does the NOC workflow close the loop?"*

**Success criteria:**
- Alert correlation via NetworkX graph topology
- Playbook suggestion engine with ranked recommendations
- Incident timeline tracking (start → escalation → resolution)
- Air-gap compliance score ≥ 95/100
- All tests pass with zero external network calls
- Full incident lifecycle completes in < 60 seconds

**Weight: 20%**

### Cross-Cutting: Documentation, Evaluation, Reproducibility
> *"Is the system documented, testable, and reproducible by someone else?"*

**Weight: 10%**

---

## 4. System Architecture (High-Level)

```
┌───────────────────────────────────────────────────────────────┐
│                    RTX 4060 Laptop (Air-Gapped)                │
│                                                               │
│  ┌─────────────────────┐    ┌──────────────────────────────┐  │
│  │   T1 (port 5173)    │    │   T2 (port 8000)             │  │
│  │   Operator Console  │    │   Alert & Solution Dashboard │  │
│  │   Three.js + anime  │    │   ECharts + anime.js         │  │
│  └─────────┬───────────┘    └────────────┬─────────────────┘  │
│            │                              │                    │
│            ▼                              ▼                    │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              T3 (port 5174) — Backend Brain            │   │
│  │  ┌──────────┐  ┌────────────┐  ┌──────────────────┐   │   │
│  │  │Device     │  │ Rule       │  │ Ollama Qwen3-8B  │   │   │
│  │  │Simulator  │  │ Engine     │  │ + ChromaDB RAG   │   │   │
│  │  └──────────┘  └────────────┘  └──────────────────┘   │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Containerlab (FRR)  ←→  Prometheus/Kafka  ←→  ML     │   │
│  └────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

### How the Three Terminals Work Together

1. **T3** continuously runs the device simulator, reports state to T1 and T2 via WebSocket
2. **T1** shows the operator the live network topology; operator can trigger actions (ping, traceroute, anomaly injection, lockdown, diagnostic mode)
3. When an anomaly fires, **T3's rule engine** detects it and sends alerts to T2
4. **T3's Ollama LLM** analyzes the alert and sends structured solutions to T2 (root cause + recommended actions)
5. **T2** displays alerts and solutions; operator can execute quick actions (lockdown, reset BGP) which go back through T3 to modify device state
6. **T1** reflects the resulting state changes on the network topology

---

## 5. Technical Requirements

### 5.1 Network Simulation
- Containerlab with FRRouting (BGP, OSPF, MPLS, LDP)
- 4 sites: Bangalore (HQ), Mumbai (DC), Chennai (DR), Delhi (Relay)
- IPsec site-to-site tunnel (Bangalore ↔ Delhi)
- TRex traffic generator for realistic data-plane load
- 7 fault scenarios: link failure, BGP flap, congestion, route leak, CRC errors, node crash, LSP break

### 5.2 Telemetry Pipeline
- Telegraf agents per router node (5s scrape interval)
- Prometheus time-series DB with alert rules
- Kafka broker for stream processing
- Elasticsearch + Kibana for log storage and visualization
- Real-time WebSocket bridge to frontends

### 5.3 ML Ensemble (7 Models)
| Model | Purpose | Input | Output |
|-------|---------|-------|--------|
| LSTM | Time-series forecasting | 60-min utilization window | 10-min prediction |
| Prophet | Trend/seasonality decomposition | 7-day hourly data | Trend, seasonality, changepoints |
| GNN | Failure propagation | Adjacency matrix + node features | Per-node failure probability |
| XGBoost | Fault classification | 18-dim feature vector | Fault type (7 classes + healthy) |
| Isolation Forest | Anomaly detection | 12-dim feature vector | Anomaly score (-1 to 1) |
| Autoencoder | Reconstruction error | 60-min metric window | Per-node reconstruction error |
| TTI Regressor | Time-to-incident | Metric deltas + rate of change | Minutes until predicted incident |

### 5.4 LLM Copilot (Ollama + RAG)
- **Primary model:** Qwen3-8B (GGUF Q4_K_M, ~5.5 GB VRAM)
- **Fallback model:** Qwen3-4B-Thinking (~2.5 GB VRAM)
- **Vector store:** ChromaDB with BAAI/bge-small-en-v1.5 embeddings
- **RAG content:** 50+ runbook documents (BGP, OSPF, MPLS, IPsec, QoS, interface troubleshooting, device recovery)
- **Output format:** Structured JSON (Q1_What, Q2_Why, Q3_How)
- **Response time:** < 10s per query on RTX 4060

### 5.5 NOC Workflow
- NetworkX graph-based alert correlation (blast radius via BFS)
- Playbook suggestion engine (tag-based matching)
- Incident timeline tracking (state transitions, severity escalations, resolution)
- Action history log

### 5.6 Air-Gap Compliance
- DNS leak detection
- HTTP proxy validation
- Process whitelist audit
- Data flow verification (no external IPs)
- Cloud credential filesystem check
- Compliance scoring (0-100, threshold ≥ 80)

---

## 6. Hardware Target

| Component | Spec |
|-----------|------|
| GPU | NVIDIA RTX 4060 (8GB VRAM) |
| CPU | AMD Ryzen 9 8945HS (8 cores / 16 threads) |
| RAM | 15 GB DDR5 |
| Storage | Local NVMe SSD |
| OS | Linux (Ubuntu 24.04) |

**VRAM budget:**
| Component | VRAM |
|-----------|------|
| Ollama Qwen3-8B (Q4_K_M) | ~5.5 GB |
| ChromaDB + embeddings | ~0.5 GB |
| ML models (loaded on demand) | ~1.0 GB |
| System reserve | ~1.0 GB |
| **Total** | **~8.0 GB** ✓ |

---

## 7. Deliverables

| Deliverable | Description |
|-------------|-------------|
| Containerlab topology | 4-site MPLS/SD-WAN with FRR, IPsec, TRex |
| Telemetry pipeline | Telegraf → Prometheus → Kafka → WebSocket |
| ML ensemble (7 models) | Trained, exported to ONNX, inferring on stream |
| Ollama + RAG copilot | Offline LLM with 50+ runbook ChromaDB index |
| NOC workflow engine | Alert correlation, playbook suggestion, incident timeline |
| Air-gap scanner | Compliance validation suite |
| Terminal 1 (T1) | 3D operator console (React + Three.js + anime.js) |
| Terminal 2 (T2) | Alert & solution dashboard (React + ECharts + anime.js) |
| Terminal 3 (T3) | Backend engine (FastAPI + WebSocket + device simulator) |
| Documentation | Architecture, build plan, per-terminal prompts, resources |

---

## 8. Boundary Conditions

### In Scope
✓ 4-site MPLS/SD-WAN network simulation (Containerlab + FRR)
✓ Prometheus/Kafka telemetry pipeline
✓ 7-model ML ensemble with ONNX export
✓ Ollama LLM with ChromaDB RAG (50+ runbooks)
✓ NetworkX-based alert correlation
✓ 3-terminal architecture (T1 operator console, T2 dashboard, T3 backend)
✓ Air-gap compliance scanner
✓ Real-time WebSocket streaming
✓ Full incident lifecycle automation

### Out of Scope
✗ Hardware deployment (simulation only)
✗ Multi-vendor NOS support (FRR only)
✗ Cloud-based ML training (all training is local)
✗ External SIEM integration
✗ Mobile app
✗ Multi-user/role-based access (single operator)
✗ Production HA/DR (single laptop deployment)

### Constraints
- **Zero cloud dependency** — no external DNS, HTTP, or API calls allowed
- **Single GPU** — RTX 4060 with 8GB VRAM shared across all services
- **14-day build window** — aggressive timeline, requires parallel development
- **Air-gapped deployment** — all dependencies must be pre-cached; no runtime internet access
- **Single operator** — no multi-user concurrency required

---

## 9. Evaluation Rubric

| Component | Weight | Minimum Pass |
|-----------|--------|-------------|
| Network Simulation (Q1) | 35% | 60% |
| ML Prediction + LLM Copilot (Q2) | 35% | 60% |
| NOC Workflow (Q3 - partial) | 10% | 60% |
| Air-Gap Integrity (Q3 - partial) | 10% | 60% |
| Documentation & Reproducibility | 10% | 60% |
| **Overall** | **100%** | **≥ 80%** |

**Scoring methodology:**
- Each component scored 0-100 based on verification criteria
- Component score × weight = weighted contribution
- Sum of all weighted contributions = overall score
- Fail if any single component < 60% OR overall < 80%

---

## 10. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Ollama Qwen3 doesn't fit RTX 4060 VRAM | Low | High | Q4 quantization tested; fallback to Qwen3-4B-Thinking |
| Containerlab incompatible with Ubuntu 24.04 | Medium | High | Test in Docker; fallback to mock simulation |
| ML models underperform with synthetic data | Medium | Medium | Hybrid approach: ML prediction + rule engine fallback |
| 14-day timeline too aggressive | Medium | Medium | Parallelize phases; mock strategies for blocked dependencies |
| WebSocket bottleneck with 2 concurrent clients | Low | Low | Async event loop handles this easily |
| Air-gap scan false positives | Low | Low | Whitelist tuning; manual override for known internal IPs |

---

## 11. Glossary

| Term | Definition |
|------|------------|
| **MPLS** | Multi-Protocol Label Switching — label-based forwarding through the network core |
| **SD-WAN** | Software-Defined Wide Area Network — overlays MPLS with IPsec/GRE tunnels |
| **FRR** | FRRouting — open-source routing protocol suite (BGP, OSPF, MPLS, LDP) |
| **Containerlab** | Container-based network emulation platform |
| **LSP** | Label Switched Path — MPLS label forwarding path through the network |
| **PE/P/CE** | Provider Edge / Provider (core) / Customer Edge — MPLS router roles |
| **RAG** | Retrieval-Augmented Generation — LLM answer generation with retrieved context |
| **Ollama** | Local LLM runtime for running models offline |
| **Qwen3** | Alibaba's large language model family (8B and 4B variants used) |
| **TRex** | Realistic traffic generator from Cisco |
| **NOC** | Network Operations Center |
| **TTI** | Time-To-Incident — how long until a predicted failure occurs |
| **GNN** | Graph Neural Network — for network topology-aware predictions |
| **ONNX** | Open Neural Network Exchange — cross-platform model format |
| **Air-Gap** | Physically isolated network with no internet connectivity |
| **Floci.io** | Local emulation of AWS services (S3, DynamoDB, Lambda) |
