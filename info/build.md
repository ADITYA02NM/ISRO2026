# 🔨 Build Guide — Step by Step

> **From zero to fully operational Air-Gapped Predictive Copilot**
>
> Estimated time: **40-60 hours** (team of 4-5)
> Prerequisites: See [resources.md](./resources.md) for tool installation links.

---

## 📋 Build Phases Overview

| Phase | Description | Duration | Dependencies |
|-------|-------------|----------|--------------|
| **0** | Environment Setup | 2-4 hours | None |
| **1** | Network Simulation | 8-12 hours | Phase 0 |
| **2** | Telemetry Pipeline | 6-8 hours | Phase 1 |
| **3** | Predictive Models | 12-16 hours | Phase 2 |
| **4** | Offline LLM Copilot | 6-10 hours | Phase 3 |
| **5** | NOC Dashboard | 8-12 hours | Phase 2, 4 |
| **6** | Integration & Validation | 4-8 hours | All above |
| **7** | Air-Gap Hardening | 2-4 hours | All above |

---

## Phase 0: Environment Setup (2-4 hours)

### Step 0.1 — System Requirements

```bash
# Verify host system
cat /etc/os-release       # Ubuntu 22.04+ or RHEL 9+
uname -r                  # Kernel 5.15+
nproc                     # 16+ cores recommended
free -h                   # 32 GB RAM min, 64 GB recommended
nvidia-smi                # Optional: GPU with 8 GB+ VRAM
df -h /                   # 100 GB+ free space
```

### Step 0.2 — Install Dependencies

```bash
# ─── Docker ───
# Ubuntu
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo usermod -aG docker $USER

# ─── Containerlab ───
sudo bash -c "$(curl -sL https://containerlab.dev/setup)" -- -y

# ─── Go (for Containerlab deps) ───
wget https://go.dev/dl/go1.22.5.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.5.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

# ─── Python 3.11+ ───
sudo apt-get install -y python3.11 python3.11-venv python3-pip

# ─── Node.js 20+ ───
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
sudo apt-get install -y nodejs

# ─── Ollama ───
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 0.3 — Clone & Initialize

```bash
git clone <your-repo-url> isro-mpls-copilot
cd isro-mpls-copilot

# Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# Create air-gapped Docker network
docker network create --driver bridge --subnet 172.20.0.0/16 airgap-net

# Create data directories
mkdir -p data/{prometheus,grafana,kafka,elasticsearch,chromadb,floci,models}
```

### Step 0.4 — Initialize SR.md

```bash
# Copy the SR.md template (see SR.md section below)
# EDIT THIS FILE with your actual credentials
cp SR.md.template SR.md
# IMPORTANT: SR.md is gitignored — never commit it
```

### Step 0.5 — Start Floci (Local AWS)

```bash
# Start Floci — our AWS replacement
docker compose -f docker/floci.yml up -d

# Verify Floci is running
curl http://localhost:4566/_localstack/health

# Run init scripts
docker exec floci-floci-1 /bin/bash /etc/localstack/init/ready.d/01-setup-infra.sh

# Verify Floci services
aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 dynamodb list-tables
```

---

## Phase 1: Network Simulation (8-12 hours)

### Step 1.1 — Deploy Topology

```bash
# Deploy the Containerlab topology
cd sim
sudo containerlab deploy --topo topology.clab.yml

# Verify all nodes are up
sudo containerlab inspect

# Expected output:
# +---+----------------+--------------+-----------------------------+
# | # |     Name       |  Kind/Image  |         IPv4 Address        |
# +---+----------------+--------------+-----------------------------+
# | 1 | clab-mpls-p1   | frr:latest   | 172.20.0.10/24             |
# | 2 | clab-mpls-p2   | frr:latest   | 172.20.0.11/24             |
# | 3 | clab-mpls-p3   | frr:latest   | 172.20.0.12/24             |
# | ... | ...          | ...          | ...                         |
```

### Step 1.2 — Configure Routing

```bash
# Apply FRRouting configs to all nodes
cd frr
./apply-configs.sh

# Verify BGP peering
docker exec clab-mpls-pe1 vtysh -c "show bgp summary"

# Verify OSPF adjacencies
docker exec clab-mpls-pe1 vtysh -c "show ip ospf neighbor"

# Verify MPLS LDP
docker exec clab-mpls-p1 vtysh -c "show mpls ldp neighbor"

# Test inter-site connectivity
docker exec clab-mpls-ce-a1 ping -c 5 10.100.2.1  # to DC network
```

### Step 1.3 — Configure IPSec Tunnels

```bash
cd ipsec
./deploy-tunnels.sh

# Verify tunnels
docker exec clab-mpls-ce-a1 ipsec status
# Expected: all tunnels show "ESTABLISHED"
```

### Step 1.4 — Deploy Traffic Generation

```bash
cd traffic

# Start TRex traffic generator
docker compose -f trex.yml up -d

# Load traffic profiles
./start-traffic.sh --profile business-mix

# Verify traffic flowing
docker exec clab-mpls-pe1 vtysh -c "show interface traffic"
```

### Step 1.5 — Validate Fault Injection

```bash
cd faults

# Quick test: inject congestion
./inject-congestion.sh --target clab-mpls-pe1 --severity medium --duration 5m

# Quick test: BGP flap
./inject-bgp-flap.sh --target clab-mpls-pe2 --duration 3m

# Verify fault captured
docker exec clab-mpls-pe1 vtysh -c "show logging last 10"
```

---

## Phase 2: Telemetry Pipeline (6-8 hours)

### Step 2.1 — Start Pipeline Services

```bash
cd telemetry

# Start the full telemetry stack
docker compose -f telemetry.yml up -d

# Verify each component
curl http://localhost:9090/-/ready          # Prometheus
curl http://localhost:9200/_cluster/health  # Elasticsearch
curl http://localhost:9092/                 # Kafka (no HTTP, but port is up)
```

### Step 2.2 — Configure Telegraf

```bash
cd telegraf

# Update SNMP community string in telegraf.conf
# (Use value from SR.md)

# Apply configuration
docker compose restart telegraf

# Verify metrics are flowing
curl http://localhost:9273/metrics | head -20
# Expected: snmp_* metrics appearing
```

### Step 2.3 — Configure Prometheus

```bash
cd prometheus

# Apply scraping configs
docker compose exec prometheus promtool check config /etc/prometheus/prometheus.yml

# Verify targets
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[].labels.job'
# Expected: telegraf, snmp, gnmi, copilot, floci
```

### Step 2.4 — Configure Kafka Streams

```bash
cd kafka

# Create topics
docker compose exec kafka kafka-topics --create --topic metrics --bootstrap-server localhost:9092
docker compose exec kafka kafka-topics --create --topic events --bootstrap-server localhost:9092
docker compose exec kafka kafka-topics --create --topic flows --bootstrap-server localhost:9092

# Verify topics
docker compose exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Start stream processor
python3 stream-processor.py --bootstrap-server localhost:9092 &
```

### Step 2.5 — Verify End-to-End Telemetry

```bash
# Inject known traffic pattern
cd sim/traffic
./start-traffic.sh --profile burst-test

# Check Prometheus has data
curl "http://localhost:9090/api/v1/query?query=rate(snmp_ifInOctets[1m])" | jq

# Check Kafka topic
docker compose exec kafka kafka-console-consumer \
  --topic metrics --bootstrap-server localhost:9092 --from-beginning --max-messages 5

# Check Elasticsearch
curl -X GET "http://localhost:9200/_search?pretty" -H 'Content-Type: application/json' \
  -d '{"query":{"match_all":{}},"size":1}'
```

---

## Phase 3: Predictive Models (12-16 hours)

### Step 3.1 — Generate Training Data

```bash
cd ml

# Run all 8 fault scenarios with ground truth logging
./run-training-scenarios.sh

# Expected output:
# - data/raw/scenario_001_congestion.csv
# - data/raw/scenario_002_bgp_flap.csv
# - data/raw/scenario_003_link_failure.csv
# ... etc

# Label and merge datasets
python3 prepare_dataset.py \
  --input data/raw/ \
  --output data/training/dataset.parquet \
  --label-source data/ground-truth/
```

### Step 3.2 — Feature Engineering

```bash
# Run feature engineering pipeline
python3 features/build_features.py \
  --input data/training/dataset.parquet \
  --output data/features/features.parquet \
  --config features/config.yaml

# Verify features
python3 features/validate_features.py --input data/features/features.parquet
```

### Step 3.3 — Train LSTM Model

```bash
# Train LSTM forecaster
python3 trainers/train_lstm.py \
  --input data/features/features.parquet \
  --output models/lstm_forecaster.pt \
  --seq-length 128 \
  --hidden-dim 256 \
  --num-layers 3 \
  --dropout 0.2 \
  --epochs 100 \
  --batch-size 64

# Training progress:
# Epoch 1/100: loss=0.4231 val_loss=0.3987
# Epoch 10/100: loss=0.2156 val_loss=0.2014
# ...
# Epoch 100/100: loss=0.0892 val_loss=0.0921

# Evaluate
python3 evaluate/evaluate_model.py \
  --model models/lstm_forecaster.pt \
  --test-data data/features/test.parquet
```

### Step 3.4 — Train Prophet Model

```bash
# Train Prophet for each key metric
python3 trainers/train_prophet.py \
  --input data/training/dataset.parquet \
  --output models/prophet/ \
  --metrics ifInOctets,ifOutOctets,latency,jitter,packet_loss

# Each metric gets its own model file:
# models/prophet/prophet_ifInOctets.pkl
# models/prophet/prophet_latency.pkl
# ...
```

### Step 3.5 — Train Graph Neural Network

```bash
# Build topology graph
python3 trainers/build_topology_graph.py \
  --topology ../sim/topology.clab.yml \
  --output data/graph/topology.pt

# Train GNN
python3 trainers/train_gnn.py \
  --graph data/graph/topology.pt \
  --features data/features/features.parquet \
  --output models/gnn_anomaly.pt \
  --hidden-dim 64 \
  --num-layers 3 \
  --epochs 100
```

### Step 3.6 — Train Ensemble (XGBoost Fusion)

```bash
# Generate meta-features from base models
python3 trainers/generate_meta_features.py \
  --lstm models/lstm_forecaster.pt \
  --prophet models/prophet/ \
  --gnn models/gnn_anomaly.pt \
  --isolation-forest models/isolation_forest.pkl \
  --input data/features/features.parquet \
  --output data/meta/meta_features.parquet

# Train XGBoost ensemble
python3 trainers/train_ensemble.py \
  --input data/meta/meta_features.parquet \
  --output models/xgboost_ensemble.json \
  --objective binary:logistic \
  --max-depth 6 \
  --learning-rate 0.05 \
  --n-estimators 200
```

### Step 3.7 — Export to ONNX

```bash
# Convert all models to ONNX for inference
python3 export_to_onnx.py \
  --models models/ \
  --output models/onnx/

# Upload to Floci S3 for persistence
aws --endpoint-url=http://localhost:4566 s3 sync models/onnx/ s3://ml-models/
```

### Step 3.8 — Validate Model Performance

```bash
# Run full evaluation suite
python3 evaluate/run_evaluation.py \
  --models models/ \
  --test-scenarios data/training/scenarios.csv

# Output summary:
# ╔════════════════════╦══════════╦════════╦════════╦════════════╗
# ║ Model              ║ Precision║ Recall ║  F1    ║ Lead Time  ║
# ╠════════════════════╬══════════╬════════╬════════╬════════════╣
# ║ LSTM               ║   0.82   ║  0.79  ║ 0.80   ║   6.2 min  ║
# ║ Prophet            ║   0.74   ║  0.71  ║ 0.72   ║   4.8 min  ║
# ║ GNN                ║   0.88   ║  0.84  ║ 0.86   ║   3.1 min  ║
# ║ XGBoost Ensemble   ║   0.91   ║  0.87  ║ 0.89   ║   7.5 min  ║
# ╚════════════════════╩══════════╩════════╩════════╩════════════╝
```

---

## Phase 4: Offline LLM Copilot (6-10 hours)

### Step 4.1 — Download & Quantize Model

```bash
# Option A: Use Ollama (easier)
cd copilot/llm

# Download Mistral 7B (once — before air-gapping)
ollama pull mistral:7b-instruct-v0.3-q4_K_M

# Verify it runs offline
ollama run mistral:7b-instruct-v0.3-q4_K_M "Hello" --nowordwrap

# Save model for offline use
ollama cp mistral:7b-instruct-v0.3-q4_K_M airgap-mistral

# Option B: Manual GGUF (for llama.cpp)
# Download GGUF:
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/mistral-7b-instruct-v0.3.Q4_K_M.gguf
mv *.gguf models/

# Create Ollama Modelfile for offline
cat > Modelfile << 'EOF'
FROM ./mistral-7b-instruct-v0.3.Q4_K_M.gguf
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_ctx 4096
EOF

ollama create airgap-mistral -f Modelfile
```

### Step 4.2 — Set Up ChromaDB

```bash
# Start ChromaDB
cd copilot/rag

# Run ChromaDB via Docker
docker run -d \
  --name chromadb \
  --network airgap-net \
  -p 8001:8000 \
  -v $(pwd)/../chroma-data:/chroma/chroma \
  chromadb/chroma:latest

# Verify
curl http://localhost:8001/api/v1/health
```

### Step 4.3 — Populate Vector Database

```bash
# Convert runbooks to embeddings
python3 populate_vector_db.py \
  --runbooks-dir ../runbooks/ \
  --db-url http://localhost:8001 \
  --collection-name network_incidents

# Verify collection
python3 query_vector_db.py \
  --db-url http://localhost:8001 \
  --query "congestion on hub link" \
  --top-k 3

# Expected output: top 3 most relevant runbooks
```

### Step 4.4 — Start Copilot API

```bash
cd copilot/api

# Configure environment
export COPILOT_API_KEY=$(grep COPILOT_API_KEY ../../SR.md | cut -d= -f2)
export OLLAMA_HOST=http://localhost:11434
export CHROMA_HOST=http://localhost:8001
export PROMETHEUS_HOST=http://localhost:9090

# Start FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2

# In production (air-gapped service):
# docker compose -f ../../docker/copilot.yml up -d
```

### Step 4.5 — Test the Copilot

```bash
# Quick health check
curl http://localhost:8000/api/v1/health

# Ask a question
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer $(grep COPILOT_API_KEY ../../SR.md | cut -d= -f2)" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the current network health status?"}'

# Expected response structure:
# {
#   "prediction": "No imminent failures detected",
#   "confidence": 0.95,
#   "time_to_impact": "N/A",
#   "root_cause_hypothesis": "...",
#   "affected_scope": { "sites": [], "services": [] },
#   "recommended_actions": []
# }
```

---

## Phase 5: NOC Dashboard (8-12 hours)

### Step 5.1 — Initialize Frontend

```bash
cd dashboard

# Install dependencies
npm install

# Required packages:
# npm install three @react-three/fiber @react-three/drei animejs
# npm install echarts echarts-for-react zustand @tanstack/react-query
# npm install tailwindcss @radix-ui/* socket.io-client

# Start development server
npm run dev
# → http://localhost:5173
```

### Step 5.2 — Configure WebSocket Connection

```typescript
// dashboard/src/hooks/useWebSocket.ts
import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

const WS_URL = import.meta.env.VITE_WS_URL || 'http://localhost:8000';

export function useWebSocket() {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const s = io(WS_URL, {
      auth: { token: import.meta.env.VITE_WS_TOKEN }
    });

    s.on('connect', () => setConnected(true));
    s.on('disconnect', () => setConnected(false));

    setSocket(s);
    return () => { s.disconnect(); };
  }, []);

  return { socket, connected };
}
```

### Step 5.3 — 3D Topology Integration

```typescript
// dashboard/src/components/three/NetworkGraph.tsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import { NodeMesh } from './NodeMesh';
import { EdgeLine } from './EdgeLine';
import { TrafficParticles } from './TrafficParticles';
import { useTopologyStore } from '../../stores/topologyStore';

export function NetworkGraph() {
  const { nodes, edges } = useTopologyStore();

  return (
    <Canvas camera={{ position: [15, 10, 15], fov: 45 }}>
      <ambientLight intensity={0.3} />
      <pointLight position={[10, 10, 10]} intensity={0.8} color="#00d4ff" />
      <Stars radius={100} depth={50} count={2000} factor={4} />
      <OrbitControls enableDamping dampingFactor={0.05} />

      {nodes.map(node => (
        <NodeMesh key={node.id} {...node} />
      ))}
      {edges.map(edge => (
        <group key={edge.id}>
          <EdgeLine {...edge} />
          <TrafficParticles {...edge} />
        </group>
      ))}
    </Canvas>
  );
}
```

### Step 5.4 — anime.js Micro-Interactions

```typescript
// dashboard/src/hooks/useAnimations.ts
import { useEffect, useRef } from 'react';
import anime from 'animejs';

export function useAlertAnimation(alertId: string, severity: string) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current || severity !== 'critical') return;

    // Critical alert pulse
    const animation = anime({
      targets: ref.current,
      scale: [1, 1.02, 1],
      boxShadow: [
        '0 0 0 rgba(239, 68, 68, 0)',
        '0 0 20px rgba(239, 68, 68, 0.4)',
        '0 0 0 rgba(239, 68, 68, 0)'
      ],
      duration: 1500,
      loop: true,
      easing: 'easeInOutSine'
    });

    return () => animation.pause();
  }, [alertId, severity]);

  return ref;
}
```

### Step 5.5 — Build & Deploy

```bash
# Production build
npm run build
# Output: dist/ directory with static files

# Serve via nginx (in air gap)
docker run -d \
  --name dashboard \
  --network airgap-net \
  -p 3000:80 \
  -v $(pwd)/dist:/usr/share/nginx/html:ro \
  nginx:alpine
```

---

## Phase 6: Integration & Validation (4-8 hours)

### Step 6.1 — Wire Components Together

```bash
# 1. Ensure all services are running
./scripts/health-check.sh

# 2. Configure copilot to pull live predictions
cd copilot/api
python3 configure_live_inference.py \
  --prometheus http://localhost:9090 \
  --model-dir ../../ml/models/onnx/ \
  --chroma http://localhost:8001

# 3. Restart copilot to pick up live mode
docker compose restart copilot-api
```

### Step 6.2 — Run Scenario Validation

```bash
# Run all 8 fault scenarios and capture results
cd sim/faults
./run_validation_suite.sh

# Results saved to: data/validation/results.csv

# Example output:
# ┌──────────────────────────────┬──────────┬──────────┬────────────┬──────────┐
# │ Scenario                     │ Lead Time│ Accuracy │ Confidence │ Response │
# ├──────────────────────────────┼──────────┼──────────┼────────────┼──────────┤
# │ Congestion buildup (95%)     │  8.2 min │   92%    │   87%      │  ⭐⭐⭐   │
# │ BGP route flap (fast)        │  4.5 min │   88%    │   82%      │  ⭐⭐⭐   │
# │ Link failure (partial)       │  2.1 min │   95%    │   91%      │  ⭐⭐⭐   │
# │ Latency injection (+300ms)   │  6.8 min │   90%    │   85%      │  ⭐⭐⭐   │
# │ Packet loss (5%)             │  5.3 min │   87%    │   83%      │  ⭐⭐    │
# │ Controller misconfig (wrong) │  1.5 min │   78%    │   74%      │  ⭐⭐    │
# │ Composite (multi-fault)      │  3.7 min │   85%    │   80%      │  ⭐⭐⭐   │
# └──────────────────────────────┴──────────┴──────────┴────────────┴──────────┘
```

### Step 6.3 — Air-Gap Verification

```bash
# Run the air-gap integrity checker
./scripts/airgap-verify.sh

# Expected: ALL PASS (0 failures)

# Also verify:
# 1. No internet-dependent packages
pip list | grep -v "installed"
# 2. No cloud SDK imports in codebase
grep -r "boto3\|awscli\|gcloud\|azure" --include="*.py" --include="*.ts" sim/ ml/ copilot/ dashboard/
```

---

## Phase 7: Air-Gap Hardening (2-4 hours)

### Step 7.1 — Bundle Docker Images

```bash
# Save all Docker images for air-gapped transport
docker save floci/floci:latest -o images/floci.tar
docker save frrouting/frr:latest -o images/frr.tar
docker save prom/prometheus:latest -o images/prometheus.tar
docker save confluentinc/cp-kafka:latest -o images/kafka.tar
docker save chromadb/chroma:latest -o images/chroma.tar
docker save ollama/ollama:latest -o images/ollama.tar
docker save nginx:alpine -o images/nginx.tar

# Verify images
ls -lh images/
```

### Step 7.2 — Bundle Python Dependencies

```bash
# Pre-download all pip packages
pip download -r requirements.txt -d packages/
tar czf python-packages.tar.gz packages/

# Save for offline installation
# On air-gapped system:
# pip install --no-index --find-links=./packages -r requirements.txt
```

### Step 7.3 — Final System Checklist

```markdown
- [ ] All containers running without errors
- [ ] Containerlab topology deployed and routing established
- [ ] Telemetry pipeline collecting from all devices
- [ ] Prometheus scraping targets all UP
- [ ] Kafka topics created and messages flowing
- [ ] Predictive models loaded and serving inference
- [ ] ChromaDB populated with runbook embeddings
- [ ] Ollama serving Mistral 7B locally (no internet)
- [ ] Copilot API responding with structured answers
- [ ] NOC Dashboard loading with 3D topology
- [ ] WebSocket real-time updates working
- [ ] Floci emulating S3, DynamoDB, SQS, Lambda, KMS
- [ ] Air-gap verification: 0 outbound dependencies
- [ ] SR.md configured with secrets but NOT in git
- [ ] .gitignore correctly excluding SR.md and secrets
```

---

## 🚀 Quick Deploy (One-Liner for Demo)

```bash
# If all artifacts are pre-built:
git clone <repo> && cd isro-mpls-copilot && make deploy && make demo
```

### Makefile Targets

```makefile
up              # Start all services
down            # Stop all services
deploy-topology # Deploy Containerlab topology
start-telemetry # Start telemetry pipeline
train-models    # Train all predictive models
start-copilot   # Start LLM copilot
dashboard       # Open NOC dashboard
health-check    # Verify all services
inject-fault    # Run fault injection scenario
query-copilot   # Ask the copilot a question
airgap-verify   # Run air-gap integrity check
demo            # Full demo sequence
```

---

> *For reference: see [main.md](./main.md) for architecture details, [resources.md](./resources.md) for tool references.*
