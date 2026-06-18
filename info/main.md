# 📐 Main Project — Deep Dive

> **Air-Gapped Predictive Copilot for Secure MPLS Operations**
>
> Everything about the core system — design decisions, component interactions, and operational workflows.

---

## 1. System Design Overview

### 1.1 Architecture Philosophy

The system follows a **layered, loosely-coupled architecture** within an air-gapped boundary:

```
┌─────────────────────────────────────────────────────────────────┐
│                    AIR-GAPPED BOUNDARY                          │
│                                                                 │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐  │
│  │Network  │──▶│Telemetry │──▶│Predictive│──▶│  LLM Copilot │  │
│  │Simulator│   │Pipeline  │   │Engine    │   │  (Offline)   │  │
│  └─────────┘   └──────────┘   └──────────┘   └──────┬───────┘  │
│                                                      │          │
│  ┌──────────┐                        ┌──────────────┴───────┐  │
│  │  Floci   │◀──────────────────────▶│  NOC Dashboard       │  │
│  │(AWS Emu) │                        │  (3D · Real-time)    │  │
│  └──────────┘                        └──────────────────────┘  │
│                                                                 │
│  ALL COMPONENTS: 0 outbound network dependencies               │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Containerlab over EVE-NG/GNS3** | Containerlab is declarative (YAML), Git-friendly, lightweight, and deployable in CI — critical for reproducible simulation |
| **FRRouting over commercial routers** | Open-source, BGP/OSPF feature-complete, Docker-native, no licensing issues |
| **Floci over AWS** | Zero cloud dependency, air-gap compliant, free, local AWS API emulation — replaces S3, DynamoDB, Lambda, SQS, KMS |
| **Qwen3-8B over larger models** | Fits entirely on RTX 4060 8 GB VRAM (Q4_K_M, 6.0 GB); 21 tok/s full GPU; Qwen3-4B-Thinking backup at 33 tok/s — no CPU offload needed |
| **ChromaDB over Pinecone/Weaviate** | Fully local, zero telemetry, MIT license, simple Python API |
| **LSTM + Prophet + GNN ensemble** | Captures temporal (LSTM), seasonal (Prophet), and topological (GNN) failure patterns — no single model covers all |
| **Kafka for stream buffer** | Decouples collection from processing; enables replay for model training |
| **Prometheus over InfluxDB** | Standard in network monitoring; integrates with Grafana natively; alert manager built-in |
| **anime.js over Framer Motion** | Lighter bundle, declarative timeline-based API, specialized for micro-interactions on data dashboards |
| **React Three Fiber over raw Three.js** | React-friendly, declarative scene graph, easier state integration |

---

## 2. Network Simulation (sim/)

### 2.1 Topology Design

```
                    ┌──────────────────────┐
                    │   Datacenter (DC)     │
                    │  P1 ─── P2 ─── P3    │
                    │  │       │       │    │
                    └──┼───────┼───────┼────┘
                       │       │       │
        ┌──────────────┼───────┼───────┼──────────────┐
        │         PE-1 ─── PE-2 ─── PE-3              │
        │              │  (MPLS Core)  │               │
        │              │               │               │
        │         CE-A │           CE-B│               │
        │         ┌────┘             └────┐           │
        │    ┌────┴────┐            ┌────┴────┐      │
        │    │Branch A1│            │Branch B1│      │
        │    │Branch A2│            │Branch B2│      │
        │    │Branch A3│            │Branch B3│      │
        │    └─────────┘            └─────────┘      │
        └─────────────────────────────────────────────┘
```

### 2.2 Node Roles

| Role | Count | Software | Function |
|------|-------|----------|----------|
| **P (Provider)** | 3 | FRR | MPLS LSR, LDP, core forwarding |
| **PE (Provider Edge)** | 3 | FRR + StrongSwan | MPLS LER, BGP/OSPF, VPN termination, IPSec |
| **CE (Customer Edge)** | 6 | FRR + StrongSwan | Site routing, SD-WAN overlay, IPSec tunnel endpoints |
| **SD-WAN Controller** | 1 | Custom Python | Policy management, tunnel orchestration |

### 2.3 Protocol Configuration

| Protocol | Role | Details |
|----------|------|---------|
| **OSPF** | IGP within sites | Area 0 backbone, per-site areas |
| **BGP** | Inter-site & MPLS VPN | iBGP full mesh between PEs, eBGP for CE |
| **MPLS LDP** | Label distribution | Dynamic label assignment |
| **IPSec** | Overlay encryption | StrongSwan IKEv2, AES-256-GCM |
| **VRF** | VPN segmentation | RED (production), BLUE (development), GREEN (guest) |
| **QoS** | Traffic shaping | LLQ on hub links, policing at edge |

### 2.4 Traffic Profiles

| Profile | Bandwidth | Protocol | Pattern |
|---------|-----------|----------|---------|
| Business-critical VoIP | 10 Mbps | RTP/UDP | Constant bitrate, bursty |
| Interactive video | 50 Mbps | RTP/UDP | Variable, meeting-driven |
| Enterprise apps | 100 Mbps | HTTPS/TCP | Office hours pattern |
| Data replication | 200 Mbps | TCP | Nightly batch |
| Web browsing | 50 Mbps | HTTPS/TCP | Random, heavy-tailed |
| Background (scans, updates) | 20 Mbps | TCP/UDP | Periodic |

### 2.5 Fault Injection Scenarios

| Scenario | Mechanism | Duration | Severity Levels |
|----------|-----------|----------|-----------------|
| **Congestion buildup** | Traffic ramping (TRex) | 10-30 min ramp | 3 (60%, 80%, 95%) |
| **BGP route flap** | Prefix withdraw/advertise cycling | 5-15 min | 2 (slow/fast) |
| **Link failure** | Interface shutdown (Containerlab) | 2-10 min | 2 (partial/full) |
| **Latency injection** | Netem delay on links | 5-20 min | 3 (+50ms, +100ms, +300ms) |
| **Packet loss** | Netem loss on links | 5-15 min | 3 (0.5%, 1%, 5%) |
| **Jitter injection** | Netem jitter on links | 5-15 min | 3 (±10ms, ±25ms, ±50ms) |
| **Controller misconfig** | Policy push with errors | 1-5 min | 2 (incomplete/wrong) |
| **Composite (multi-fault)** | Sequential fault chain | 15-45 min | Custom |

---

## 3. Telemetry Pipeline (telemetry/)

### 3.1 Data Flow

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Devices  │──▶│Telegraf  │──▶│  Kafka   │──▶│  Stream  │──▶│ Storage  │
│ (SNMP/   │   │(SNMP/    │   │ Topics:  │   │ Processor│   │ Layer    │
│  gNMI/   │   │ gNMI/    │   │ metrics  │   │(Kafka    │   │(Prom/ES/ │
│  syslog) │   │ syslog)  │   │ events   │   │ Streams) │   │ Loki)    │
└──────────┘   └──────────┘   │ flows    │   └──────────┘   └──────────┘
                              └──────────┘
```

### 3.2 Telegraf Inputs

```toml
# SNMP polling from all routers
[[inputs.snmp]]
  agents = ["udp://172.20.0.10:161", "udp://172.20.0.11:161"]
  version = 2
  community = "public"

  [[inputs.snmp.field]]
    name = "ifInOctets"
    oid = "1.3.6.1.2.1.2.2.1.10"

  [[inputs.snmp.field]]
    name = "ifOutOctets"
    oid = "1.3.6.1.2.1.2.2.1.16"

  [[inputs.snmp.field]]
    name = "ifErrors"
    oid = "1.3.6.1.2.1.2.2.1.14"

# gNMI streaming from SD-WAN controller
[[inputs.gnmi]]
  addresses = ["172.20.0.100:57400"]
  username = "admin"
  password = "${GNMI_PASSWORD}"

  [[inputs.gnmi.subscription]]
    path = "/interfaces/interface/state/counters"
    mode = "sample"
    sample_interval = "5s"

# Syslog events
[[inputs.syslog]]
  server = "tcp://0.0.0.0:6514"
  best_effort = true
```

### 3.3 Prometheus Alerting Rules

```yaml
groups:
  - name: network_anomalies
    rules:
      # LSTM prediction - high congestion probability
      - alert: PredictedCongestion
        expr: lstm_congestion_probability > 0.7
        for: 2m
        annotations:
          summary: "LSTM predicts congestion on {{ $labels.interface }}"
          lead_time: "{{ $value | humanizeDuration }}"

      # Prophet forecast deviation
      - alert: TrafficAnomaly
        expr: abs(traffic_actual - prophet_forecast) / prophet_forecast > 0.3
        for: 5m
        annotations:
          summary: "Traffic deviates >30% from Prophet forecast"

      # Graph-based anomaly score
      - alert: TopologyAnomaly
        expr: gnn_anomaly_score > 0.8
        for: 1m
        annotations:
          summary: "GNN detected topology anomaly on {{ $labels.site }}"
```

---

## 4. Predictive Engine (ml/)

### 4.1 Model Architecture

```
                  ┌─────────────────────────────────────────┐
                  │         Raw Telemetry Stream            │
                  └──────────┬──────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │ Feature Pipeline │
                    │  · Rolling stats │
                    │  · FFT features  │
                    │  · Graph embeds  │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────────┐
         ▼                   ▼                       ▼
   ┌──────────┐       ┌──────────┐           ┌──────────────┐
   │   LSTM   │       │  Prophet │           │   GNN (PyG)  │
   │  Forecaster│     │Forecaster│           │Topology-Aware│
   │ congestion│      │ baseline │           │Anomaly Detect│
   │ latency   │      │ seasonal │           │   Node-level │
   │ utilization│     │ patterns │           │ Edge-level   │
   └─────┬─────┘      └────┬─────┘           └──────┬───────┘
         │                 │                        │
         └─────────────────┼────────────────────────┘
                           ▼
                  ┌──────────────────┐
                  │  XGBoost Fusion  │
                  │  Ensemble Layer  │
                  │  · Calibrated    │
                  │  · Meta-features │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │  Final Prediction│
                  │  · Type          │
                  │  · Probability   │
                  │  · Time-to-impact│
                  └──────────────────┘
```

### 4.2 Training Configuration

| Model | Input Features | Sequence Length | Training Time (GPU) | Inference Time |
|-------|---------------|-----------------|---------------------|----------------|
| **LSTM** | 32 features (ifOctets, ifErrors, latency, jitter, BGP events...) | 128 steps (10.6 min @ 5s) | ~45 min / 100 epochs | ~5ms / batch |
| **Prophet** | Single metric time-series | Full history | ~10 min / metric | ~2ms |
| **GNN** | Node features (16-dim) + adjacency matrix | Snapshot | ~60 min / 100 epochs | ~8ms |
| **Isolation Forest** | 64-dim feature vector | N/A (stateless) | ~5 min | ~1ms |
| **XGBoost Ensemble** | 8 meta-features (model outputs) | N/A | ~15 min | <1ms |

### 4.3 Evaluation Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Precision** | > 0.85 | TP / (TP + FP) |
| **Recall** | > 0.80 | TP / (TP + FN) |
| **F1 Score** | > 0.82 | 2 × P × R / (P + R) |
| **Mean Lead Time** | > 5 min | Avg time from prediction to threshold breach |
| **False Alarm Rate** | < 0.15 | FP / total predictions |
| **TTI Error** | < 20% | |predicted - actual| / actual × 100 |
| **ROC-AUC** | > 0.90 | Area under ROC curve |

---

## 5. Offline LLM Copilot (copilot/)

### 5.1 Copilot Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Copilot API (FastAPI)                    │
│                                                                 │
│  POST /api/v1/chat                                              │
│  { query: "What is likely to fail next?" }                      │
│                                                                 │
│  ┌───────────┐    ┌──────────────┐    ┌─────────────────────┐  │
│  │ Context   │───▶│ RAG Pipeline │───▶│ LLM Inference       │  │
│  │ Builder   │    │ · ChromaDB   │    │ (Qwen3-8B ·       │  │
│  │           │    │ · Similarity │    │  llama.cpp)         │  │
│  └───────────┘    │ · Retrieved  │    └──────────┬──────────┘  │
│                   │   runbooks   │               │             │
│                   └──────────────┘               ▼             │
│                                        ┌──────────────────┐    │
│                                        │ Response         │    │
│                                        │ Formatter        │    │
│                                        │ · JSON struct    │    │
│                                        │ · Actions        │    │
│                                        └──────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Prompt Template

```system
You are NOC Copilot — an AI assistant for network operations operating
inside an air-gapped environment. You have access to:

1. Live telemetry data from the SD-WAN/MPLS network
2. Predictive model outputs (LSTM, Prophet, GNN)
3. Historical incident data from the runbook database
4. Network topology metadata

Always respond in this JSON structure:
{
  "prediction": "Brief description of predicted issue",
  "confidence": 0.0-1.0,
  "time_to_impact": "Estimated time before SLA breach",
  "root_cause_hypothesis": "What signals indicate this issue",
  "affected_scope": { "sites": [...], "services": [...] },
  "recommended_actions": [
    { "action": "...", "priority": "high|medium|low", "playbook_ref": "..." }
  ]
}

If you cannot make a prediction with confidence > 0.3, state that clearly.
Do NOT reference any external data sources, cloud services, or internet resources.
Ground all responses in the provided context only.
```

### 5.3 RAG Collection Schema

```
Collection: network_incidents
┌─────────────┬──────────────┬──────────────┬────────────────────┐
│ Field       │ Type         │ Embed        │ Description         │
├─────────────┼──────────────┼──────────────┼────────────────────┤
│ incident_id │ string       │ No           │ Unique identifier   │
│ title       │ string       │ Yes (embed)  │ Incident title      │
│ description │ string       │ Yes (embed)  │ Full description    │
│ symptoms    │ string[]     │ Yes          │ Observed symptoms   │
│ root_cause  │ string       │ Yes (embed)  │ Determined cause    │
│ resolution  │ string       │ No           │ Resolution steps    │
│ severity    │ string       │ No           │ CRITICAL/HIGH/MED   │
│ site        │ string       │ No           │ Site identifier     │
│ devices     │ string[]     │ No           │ Affected devices    │
│ timestamp   │ datetime     │ No           │ When it occurred    │
│ duration    │ string       │ No           │ Resolution time     │
│ tags        │ string[]     │ Yes          │ Categorization tags │
└─────────────┴──────────────┴──────────────┴────────────────────┘
```

### 5.4 Quantization Configuration

```yaml
# ─── Primary Model ───
model: Qwen/Qwen3-8B
quantization: GGUF Q4_K_M
inference_engine: Ollama / llama.cpp (CUDA)

# Hardware: RTX 4060 Laptop 8 GB VRAM / Ryzen 9 8945HS / 15 GB RAM
# Qwen3-8B Q4_K_M: fits entirely on GPU at 6.0 GB VRAM (~21 tok/s)
# Qwen3-4B-Thinking Q5_K_M: backup at 3.9 GB VRAM (~33 tok/s)

# CPU Mode (llama.cpp GGUF — for CPU-only fallback)
parameters:
  context_length: 4096
  batch_size: 512
  threads: 8
  gpu_layers: 0  # CPU only

# GPU Mode (Ollama with CUDA — default config)
parameters:
  context_length: 4096
  batch_size: 2048
  gpu_layers: 35  # All layers on GPU (8B model fits fully)
  tensor_split: [0, 0]  # Single GPU (RTX 4060)

# Performance targets (measured on dev machine):
# RTX 4060 8GB:   ~21 tokens/sec (Qwen3-8B Q4_K_M)
# RTX 4060 8GB:   ~33 tokens/sec (Qwen3-4B-Thinking Q5_K_M)
# CPU only (8C):  ~3-5 tokens/sec (slow, inference only)
```

---

## 6. Floci Integration (floci/)

### 6.1 Why Floci Instead of AWS

The challenge requires an **air-gapped** solution. Floci provides:

| AWS Service | Floci Local Equivalent | Purpose in Project |
|-------------|----------------------|-------------------|
| **S3** | `http://localhost:4566` | Model artifact storage, runbook storage |
| **DynamoDB** | `http://localhost:4566` | Incident records, alert state, prediction registry |
| **Lambda** | Docker-backed | Automated remediation actions, playbook execution |
| **SQS** | `http://localhost:4566` | Alert event bus, inter-component messaging |
| **KMS** | `http://localhost:4566` | Local encryption keys for secrets |
| **Secrets Manager** | `http://localhost:4566` | Manage local credentials |

### 6.2 Floci Compose Configuration

```yaml
# docker/floci.yml
services:
  floci:
    image: floci/floci:latest-compat
    ports:
      - "4566:4566"
    environment:
      - FLOCI_STORAGE_MODE=persistent
      - FLOCI_DEFAULT_REGION=us-east-1
      - FLOCI_DEFAULT_ACCOUNT_ID=000000000000
      - FLOCI_HOSTNAME=floci
      - FLOCI_SERVICES_LAMBDA_DOCKER_NETWORK=airgap-net
    volumes:
      - floci-data:/var/lib/floci
      - ./floci/init-scripts:/etc/localstack/init/ready.d
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - airgap-net
    restart: unless-stopped

volumes:
  floci-data:

networks:
  airgap-net:
    external: true
```

### 6.3 Init Scripts

```bash
#!/bin/bash
# init-scripts/01-setup-infra.sh
# Runs when Floci is ready (auto-executed)

# Create S3 buckets for model artifacts
aws --endpoint-url=http://localhost:4566 s3 mb s3://ml-models
aws --endpoint-url=http://localhost:4566 s3 mb s3://runbooks
aws --endpoint-url=http://localhost:4566 s3 mb s3://telemetry-archive

# Create DynamoDB tables
aws --endpoint-url=http://localhost:4566 dynamodb create-table \
  --table-name incidents \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

aws --endpoint-url=http://localhost:4566 dynamodb create-table \
  --table-name predictions \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# Create SQS queues
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name alert-events
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name telemetry-stream

# Generate local KMS key
aws --endpoint-url=http://localhost:4566 kms create-key \
  --description "Air-gapped master key"
```

---

## 7. Air-Gap Verification

### 7.1 Verification Script

```bash
#!/bin/bash
# scripts/airgap-verify.sh

FAILURES=0

echo "🔒 Air-Gap Integrity Verification"
echo "=================================="

# 1. Check no outbound DNS queries from runtime containers
for container in $(docker ps --format '{{.Names}}'); do
  if docker exec $container nslookup google.com 2>/dev/null | grep -q "Address:"; then
    echo "❌ FAIL: $container can resolve external DNS"
    FAILURES=$((FAILURES + 1))
  else
    echo "✅ PASS: $container has no external DNS"
  fi
done

# 2. Check no external IP connectivity
for container in $(docker ps --format '{{.Names}}'); do
  if docker exec $container ping -c 1 -W 2 8.8.8.8 2>/dev/null | grep -q "1 received"; then
    echo "❌ FAIL: $container can reach external IP"
    FAILURES=$((FAILURES + 1))
  else
    echo "✅ PASS: $container cannot reach external IP"
  fi
done

# 3. Verify all LLM inference is local
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
  echo "✅ PASS: Ollama running locally"
else
  echo "❌ FAIL: Ollama not accessible"
  FAILURES=$((FAILURES + 1))
fi

# 4. Verify Floci (no auth token needed)
if curl -s http://localhost:4566/_localstack/health > /dev/null 2>&1; then
  echo "✅ PASS: Floci emulator running locally"
else
  echo "❌ FAIL: Floci not accessible"
  FAILURES=$((FAILURES + 1))
fi

# 5. Verify no cloud SDK endpoints configured
if grep -r "amazonaws.com\|googleapis.com\|azure.com" \
  --include="*.py" --include="*.ts" --include="*.yaml" \
  --include="*.toml" --include="*.conf" sim/ telemetry/ ml/ copilot/ dashboard/ 2>/dev/null; then
  echo "❌ FAIL: Found cloud endpoint references in source code"
  FAILURES=$((FAILURES + 1))
else
  echo "✅ PASS: No cloud endpoints referenced in source"
fi

echo ""
if [ $FAILURES -eq 0 ]; then
  echo "✅ ALL PASS — Air-gap integrity confirmed"
  exit 0
else
  echo "❌ $FAILURES FAILURES — Air-gap integrity compromised"
  exit 1
fi
```

---

## 8. Operational Workflows

### 8.1 Incident Response Flow

```
1. Telemetry deviation detected
   ↓
2. Predictive models generate alert with confidence + TTI
   ↓
3. Alert published to SQS alert-events queue
   ↓
4. Copilot API triggered: fetches context + runbooks
   ↓
5. LLM generates structured response with actions
   ↓
6. Dashboard displays alert + copilot recommendation
   ↓
7. Operator reviews, approves/overrides action
   ↓
8. Lambda executes automated remediation (if approved)
   ↓
9. Post-incident summary written to DynamoDB
   ↓
10. Runbook updated (if new resolution pattern found)
```

### 8.2 Operator Query Examples

```bash
# What's going to fail?
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer $(cat SR.md | grep COPILOT_API_KEY | cut -d= -f2)" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is likely to fail in the next 15 minutes?"}'

# Investigate specific prediction
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer $(cat SR.md | grep COPILOT_API_KEY | cut -d= -f2)" \
  -H "Content-Type: application/json" \
  -d '{"query": "Why is site B at risk? Show me the contributing signals."}'

# Get remediation steps
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer $(cat SR.md | grep COPILOT_API_KEY | cut -d= -f2)" \
  -H "Content-Type: application/json" \
  -d '{"query": "What should I do about the predicted congestion on PE-1?"}'
```

---

## 9. Performance Targets

| Metric | Target | Measured By |
|--------|--------|-------------|
| Prediction lead time | > 5 minutes before threshold breach | Fault scenario logs |
| Copilot response time | < 5 seconds (end-to-end) | API timestamps |
| Dashboard render time | < 2 seconds initial load | Lighthouse |
| Telemetry end-to-end latency | < 10 seconds | Timestamp deltas |
| Floci API response | < 100ms (in-memory) | Prometheus latency |
| System uptime | > 99.9% (air-gap isolated) | Prometheus |
| Air-gap compliance | 100% zero outbound calls | `airgap-verify.sh` |

---

> *Next: See [build.md](./build.md) for step-by-step build instructions.*
> *See [resources.md](./resources.md) for the complete resource index.*
