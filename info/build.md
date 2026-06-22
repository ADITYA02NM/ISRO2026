# Build Plan — PS13 (6 Phases)

14-day solo build of the Air-Gapped Predictive Copilot for Secure MPLS Operations. Each phase includes mock strategy (for development without real hardware), frontend integration points, and verification criteria.

---

## Phase 1: Network Simulation

**Goal**: Running Containerlab topology with FRRouting BGP/OSPF/MPLS/LDP, IPsec tunnels, TRex traffic, and 7 fault injection scenarios.

**Duration**: Days 1–3

### Tasks
1. Install Containerlab + pull FRR, StrongSwan, TRex Docker images
2. Define `topology.clab.yml` with 4 sites, 12+ router nodes
3. Write FRR configs per router:
   - P1, P2, P3: Core MPLS with LDP, iBGP to PE peers
   - PE1, PE2, PE3: MPLS edge with eBGP to CE, OSPF to P-core
   - CE1, CE2, CE3: Standard IP routing, eBGP to PE
   - IPsec Gateways: StrongSwan site-to-site config
4. Generate TRex traffic profile (realistic data-plane load)
5. Implement 7 fault injection scripts (`bash + clab exec`)
6. Write FastAPI orchestrator for start/stop/reset/inject

### Mock Strategy (pre-Containerlab)
- Use pre-recorded telemetry snapshots (JSON files in `simulation/scripts/`)
- Backend returns mock topology state from static JSON with simulated transitions
- Frontend develops against mock REST + WS responses

### Verification
- `clab deploy` succeeds, all 12+ containers reachable
- BGP sessions established: `show ip bgp summary` on all PE routers
- MPLS LSPs operational: `show mpls lsp` on all routers
- IPsec tunnel established: `ipsec status` on gateways
- TRex generates >100K pps traffic
- All 7 fault scenarios inject and revert correctly

---

## Phase 2: Telemetry Pipeline

**Goal**: Telegraf → Prometheus → Kafka → ELK pipeline collecting metrics from simulation and streaming to ML engine.

**Duration**: Days 3–5

### Tasks
1. Deploy Prometheus + configure scrape targets (Containerlab Docker labels)
2. Deploy Telegraf agents per router node (interface counters, CPU, BGP state)
3. Deploy Kafka broker + create topics (metrics, alerts, events)
4. Deploy Elasticsearch + Kibana for log storage and visualization
5. Configure Prometheus alert rules for baseline thresholds
6. Write Kafka consumer in FastAPI that forwards metrics to WebSocket
7. Build telemetry dashboard queries (Kibana saved objects)

### Mock Strategy (pre-simulation)
- Telegraf → Prometheus runs in Docker with synthetic metric generator
- Backend generates Prometheus-format metrics from script with simulated patterns
- Kafka consumer bridges mock data to ML engine for development

### Verification
- Prometheus scrapes all targets (up metric = 1 for all)
- Kafka topic messages flowing (producer → consumer confirmed)
- Elasticsearch indexed documents queryable
- Alert rules fire at configured thresholds
- WS bridge delivers metrics to dashboard within 1s of scrape

---

## Phase 3: Predictive ML Ensemble

**Goal**: 7 trained models (LSTM, Prophet, GNN, XGBoost, Isolation Forest, Autoencoder, TTI Regressor) exported to ONNX, running inference on telemetry stream.

**Duration**: Days 5–8

### Tasks

#### Model Development

**LSTM (Time-Series)**:
- Input: 60-minute window of interface utilization (5s resolution → 720 points)
- Output: Next 10-minute utilization prediction per interface
- Architecture: 3-layer LSTM (128→64→32) + Dense(1)
- Training: Synthetic data from TRex patterns + augmented with fault signatures
- ONNX export: Torch -> ONNX with dynamic axes

**Prophet (Trend/Seasonality)**:
- Input: 7-day hourly utilization (synthetic)
- Output: Trend, weekly/daily seasonality, changepoints
- Training: Log-normal noise added to TRex patterns
- Saved as: pickle + JSON model parameters (ONNX not viable for Prophet)

**GNN (Graph Neural Network)**:
- Input: Topology adjacency matrix + node features (utilization, errors, BGP state)
- Output: Per-node failure propagation probability
- Architecture: 3-layer GCN (64→32→16) + edge-aware attention
- Training: Simulated fault propagation traces
- ONNX export: PyG -> ONNX

**XGBoost (Classifier)**:
- Input: 18 telemetry features (utilization, errors, CPU, BGP prefixes, etc.)
- Output: Fault type (7 classes + "healthy")
- Training: Labeled dataset from fault injection runs
- Saved as: XGBoost binary model

**Isolation Forest (Anomaly)**:
- Input: 12-dimensional feature vector per node
- Output: Anomaly score (-1 to 1)
- Training: Fit on "healthy" telemetry baseline
- Saved as: sklearn pickle -> ONNX (skl2onnx)

**Autoencoder (Reconstruction Error)**:
- Input: 60-minute window of metrics (100-dim latent space)
- Output: Reconstruction error per node
- Architecture: 100→50→25→50→100
- Training: Healthy data only (anomalies = high reconstruction error)
- ONNX export: Torch -> ONNX

**TTI Regressor (Time-to-Incident)**:
- Input: Current metric deltas + rate of change
- Output: Minutes remaining before predicted incident
- Architecture: XGBoost regressor
- Training: Labeled fault evolution traces
- Saved as: XGBoost binary model

#### Integration
1. Model loader service in `ml/` directory
2. Batch inference pipeline (every 30s on Prometheus data)
3. Event-driven inference (on alert trigger)
4. ONNX runtime wrapper for all exported models
5. Kafka producer for prediction results

### Mock Strategy (pre-trained)
- Rule-based heuristics simulate model predictions (e.g., "if utilization > 80%, predict failure probability 0.6")
- Pre-generated prediction JSON files for dashboard development
- Model training runs in parallel with Phase 1-2; inference mock during training

### Verification
- All 7 models load and produce predictions within 5s
- ONNX inference matches PyTorch/sklearn inference (within 1e-5 tolerance)
- Batch pipeline produces predictions every 30s
- Event-driven inference completes within 2s of alert
- Prediction results available on WS within 500ms

---

## Phase 4: Offline LLM Copilot

**Goal**: Qwen3-8B running via Ollama with ChromaDB RAG over 50+ internal runbook documents, producing structured Q1/Q2/Q3 answers.

**Duration**: Days 8–10

### Tasks
1. Install Ollama + pull Qwen3-8B and Qwen3-4B-Thinking models
2. Create 50+ runbook documents in `llm/runbooks/` (markdown):
   - BGP troubleshooting (flap, convergence, prefix limits)
   - OSPF troubleshooting (adjacency, LSDB corruption)
   - MPLS troubleshooting (LSP break, label mismatch, TTL expiry)
   - IPsec troubleshooting (SA mismatch, rekey failure)
   - Interface troubleshooting (CRC errors, duplex mismatch, flapping)
   - Congestion management (QoS, shaping, policing)
   - Device recovery (crash, restart, config restore)
3. Build ChromaDB ingestion pipeline:
   - Chunk runbooks into 512-token segments (LangChain RecursiveCharacterTextSplitter)
   - Embed with Qwen3-8B (or BAAI/bge-small-en-v1.5)
   - Store in persistent ChromaDB collection
4. Build RAG pipeline:
   - Query → embed → ChromaDB similarity search (top-5 chunks)
   - Prompt template: system context + retrieved chunks + telemetry data
   - LLM generate → parse structured JSON response
   - Validate JSON schema (Q1_What, Q2_Why, Q3_How)
5. Implement Ollama model selection:
   - Default: Qwen3-8B (full reasoning)
   - Fallback: Qwen3-4B-Thinking (when VRAM < 4GB available)
6. Build API: `POST /api/copilot/query` with streaming response
7. Implement auto-trigger: ML prediction > threshold → auto-query copilot

### Mock Strategy (pre-Ollama)
- Simulated LLM responses from pre-written JSON for common scenarios
- Rule-based template filling for Q1/Q2/Q3 (no actual LLM calls)
- ChromaDB populated with 10 sample runbooks for development

### Verification
- Ollama serves Qwen3-8B at acceptable speed (< 10s per query on RTX 4060)
- RAG retrieval returns relevant runbooks for 10 test queries (precision@5 > 0.8)
- Structured JSON output validates against schema
- Auto-trigger fires when prediction confidence > 0.8
- Fallback model activates correctly when VRAM constrained

---

## Phase 5: NOC Workflow Automation

**Goal**: Alert correlation via NetworkX graph, playbook suggestion engine, incident timeline summarization.

**Duration**: Days 10–12

### Tasks
1. Build NetworkX graph from Containerlab topology:
   - Nodes: all router/device entries
   - Edges: all links with bandwidth, latency metadata
   - Node attributes: role, site, BGP peers, MPLS neighbors
2. Implement alert correlator:
   - Maintain sliding window (last 5 minutes of alerts)
   - Compute blast radius per alert via BFS on graph
   - Group alerts sharing > 50% blast radius + temporal proximity
3. Build playbook suggestion engine:
   - Tag each runbook with applicable alert types + device roles
   - On incident: match alert types + device roles to runbook tags
   - Rank by match score (number of tags matched / total tags)
4. Implement incident timeline:
   - Track all alert state transitions per incident
   - Log duration, severity escalations, resolution steps
   - Store in floci.io DynamoDB (incidents table)
5. Build API endpoints for workflow queries

### Mock Strategy
- NetworkX graph built from static topology JSON
- Alert correlator runs on pre-recorded alert sequences
- Playbook matching uses runbook metadata only (no LLM)

### Verification
- NetworkX graph matches topology (correct node/edge count)
- Blast radius computed correctly for single-link and multi-link failures
- Alert groups correctly correlated (test with 3 simultaneous faults)
- Playbook suggestion ranks correct playbook in top-3 for 5 test scenarios
- Incident timeline correctly tracks lifecycle (start → escalation → resolution)

---

## Phase 6: Air-Gap Scanner + Validation

**Goal**: Air-gap integrity scanner and full end-to-end validation of all phases.

**Duration**: Days 12–14

### Tasks
1. Build air-gap scanner:
   - DNS leak detection: test resolution of 10 known external domains
   - HTTP proxy validation: check env vars + test external HTTP GET (must fail)
   - Process audit: whitelist-based process list comparison
   - Data flow verification: parse `ss -tuanp` output, flag external IPs
2. Build compliance scoring:
   - Each check: pass (25 pts), warning (10 pts), fail (0 pts)
   - Total: 0-100 scale, threshold >= 80 = compliant
3. Create validation suite:
   - Phase 1: Deploy topology, verify all BGP peers established
   - Phase 2: Inject metrics, verify Kafka topic flow
   - Phase 3: Run inference, verify predictions match expectations
   - Phase 4: Query copilot, verify structured output
   - Phase 5: Inject faults, verify correlation + playbook suggestion
   - Phase 6: Run scanner, verify compliant state
4. Integration test: Full incident lifecycle (T+0 to resolution)
5. Performance benchmark: Inference latency, pipeline throughput, WS message rate

### Mock Strategy
- Scanner runs against actual system state (no mocking needed for final phase)
- Validation suite uses container simulation for repeatable tests

### Verification
- All 6 phases validated end-to-end
- Air-gap scanner reports ≥ 95 score in compliant state
- Full incident lifecycle completes in < 1 minute
- Inference pipeline handles 100+ metrics per second
- WS delivers updates to both dashboards with < 200ms latency
- All tests pass with zero cloud dependencies

---

## Build Sequence Diagram

```
Day 1    2    3    4    5    6    7    8    9    10   11   12   13   14
├──── Phase 1 ────┤
│   Containerlab   │
│   FRR + IPsec    │
│   Fault scripts  │
└─────────────────┘
     ├──────── Phase 2 ────────┤
     │  Telegraf → Prometheus  │
     │  Kafka → ELK           │
     └────────────────────────┘
          ├──────────── Phase 3 ────────────────┤
          │  ML model training (runs parallel)  │
          │  Model export + integration         │
          └────────────────────────────────────┘
               ├──────── Phase 4 ─────────┤
               │  Ollama + RAG pipeline    │
               │  Structured Q1/Q2/Q3     │
               └───────────────────────────┘
                    ├───── Phase 5 ───────┤
                    │  NetworkX corr.      │
                    │  Playbook engine     │
                    └──────────────────────┘
                         ├── Phase 6 ──┤
                         │ Air-gap     │
                         │ Validation  │
                         └─────────────┘
```

---

## Prerequisites

- Docker + docker-compose installed
- Containerlab installed (or WSL2 on Windows)
- NVIDIA driver + CUDA 12.x (for RTX 4060)
- Ollama installed
- Python 3.11+ with PyTorch, scikit-learn, NetworkX
- Node.js 20+ for frontends
- floci.io CLI + local emulation configured
- No cloud accounts required
