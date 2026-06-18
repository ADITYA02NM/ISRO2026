# 🛰️ Air-Gapped Predictive Copilot for Secure MPLS Operations

**ISRO Bharatiya Antariksh Hackathon 2026 — Challenge 13**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Floci](https://img.shields.io/badge/infra-floci.io-orange)](https://floci.io)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)
[![Containerlab](https://img.shields.io/badge/netlab-containerlab-important)](https://containerlab.dev)

> **Predict network failures *before* they impact operations — entirely within an air-gapped environment.**

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Key Features](#-key-features)
- [Architecture Overview](#-architecture-overview)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [Security & Air-Gap Compliance](#-security--air-gap-compliance)
- [Evaluation Criteria](#-evaluation-criteria)
- [Team](#-team)
- [License](#-license)

---

## 🎯 Problem Statement

Modern enterprise and government networks rely on SD-WAN deployments running over MPLS underlays. As these networks grow in complexity, operational visibility and response speed become critical — yet **conventional NOC tooling remains reactive**.

**Two compounding challenges:**

| Challenge | Impact |
|-----------|--------|
| **Reactive detection** | Threshold-based alerts fire *after* performance breaches — no time for pre-emptive intervention |
| **Air-gap constraints** | Regulated environments prohibit cloud-connected AI, leaving operators without intelligent guidance |

### What We Built

An **autonomous, air-gapped AI NOC Copilot** that:

1. ✅ Simulates a realistic multi-site SD-WAN/MPLS topology with fault injection
2. ✅ Predicts network failures using ML (LSTM, Prophet, graph anomaly detection)
3. ✅ Runs a fully offline quantized LLM (Qwen3-8B / Qwen3-4B-Thinking) with RAG over internal runbooks
4. ✅ Answers three critical questions in real time:
   - **Q1:** *What is likely to fail next — and when?*
   - **Q2:** *Why is risk elevated — which signals contributed?*
   - **Q3:** *What corrective action should be taken before SLA or security impact occurs?*

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔮 **Predictive Fault Analytics** | LSTM + Prophet + graph-based anomaly detection with configurable lead-time targets |
| 🤖 **Offline LLM Copilot** | Quantized Qwen3-8B / Qwen3-4B-Thinking with local RAG — zero cloud dependency |
| 🌐 **Realistic Network Simulation** | Containerlab-based multi-site topology (branch/hub/datacenter) with MPLS, BGP, IPSec |
| 📊 **NOC Dashboard** | 3D WebGL dashboard with anime.js micro-interactions, real-time telemetry overlays |
| 🔐 **Air-Gap First Design** | All inference, storage, and retrieval operates within the air-gapped boundary |
| ⚡ **Floci-Powered Cloud Emulation** | AWS services emulated locally via [floci.io](https://github.com/floci-io/floci) — no cloud account needed |
| 🧪 **Fault Injection Engine** | Programmatic congestion, route flaps, link failures, and controller misconfigurations |
| 📈 **Time-to-Impact Estimation** | Actionable lead-time windows before predicted service breach |

---

## 🏗 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AIR-GAPPED BOUNDARY                              │
│  ┌──────────┐   ┌──────────────┐   ┌───────────────────────────┐   │
│  │Network   │──▶│ Telemetry    │──▶│ Predictive Engine         │   │
│  │Simulation│   │ Pipeline     │   │ (LSTM · Prophet · Graph)  │   │
│  │(Container│   │ (Telegraf →  │   └────────────┬──────────────┘   │
│  │  -lab)   │   │  Prometheus  │                │                   │
│  └──────────┘   │  → Kafka)    │                ▼                   │
│                 └──────────────┘   ┌───────────────────────────┐   │
│                                    │    LLM Copilot (Offline)  │   │
│  ┌──────────┐                      │  Qwen3-8B · RAG · QA   │   │
│  │Fault     │─────────────────────▶│  ChromaDB · LangChain    │   │
│  │Injection │                      └────────────┬──────────────┘   │
│  │Engine    │                                   │                   │
│  └──────────┘                                   ▼                   │
│                                      ┌───────────────────────┐     │
│                                      │   NOC Dashboard       │     │
│                                      │   (3D · WebGL ·       │     │
│                                      │    anime.js · Grafana)│     │
│                                      └───────────────────────┘     │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Floci (Local AWS Emulation)                                 │  │
│  │  S3 · DynamoDB · Lambda · SQS · KMS · Secrets Manager       │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

> **All components live within the air-gapped boundary.** No outbound network calls, no cloud API dependencies.

---

## 🗺 Development Roadmap

> **Solo developer strategy — build one role at a time, session by session.**

### 👤 Role Strategy (Solo Developer)

You'll wear four hats across 10 build sessions. Each session is designed to be **completed independently** with clear deliverables.

| Role | Sessions | What You Build |
|------|----------|----------------|
| 🌐 **Network Engineer** | 1–3 | Containerlab topology, FRRouting (BGP/OSPF/MPLS), IPSec tunnels, TRex traffic generation, fault injection engine |
| 📊 **Telemetry & ML Engineer** | 4–6 | Telegraf/Prometheus/Kafka pipeline, LSTM forecaster, Prophet seasonal model, GNN anomaly detection, XGBoost ensemble fusion |
| 🤖 **LLM & RAG Engineer** | 7–8 | Ollama + Qwen3-8B (quantized), ChromaDB vector store, LangChain RAG pipeline, FastAPI copilot with WebSocket |
| 🎨 **Frontend & Infrastructure** | 9–10 | NOC Dashboard (React + Three.js 3D + anime.js + ECharts), Floci local AWS integration, air-gap hardening, full validation |

### 📐 Interface Contracts (Decoupled Architecture)

Each layer communicates through well-defined interfaces. Build and test against **mocked versions** first, then connect real components in Session 10.

| ID | Interface | Direction | Format | What Passes |
|----|-----------|-----------|--------|-------------|
| IF-01 | Topology → Telemetry | Network → Pipeline | SNMP/gNMI metrics | Interface counters, BGP events, latency probes |
| IF-02 | Telemetry → ML | Pipeline → Engine | Feature vectors (CSV/Parquet) | 32-dim time-windowed features with labels |
| IF-03 | ML → LLM Copilot | Engine → API | JSON prediction event | `{ type, probability, tti, affected_scope }` |
| IF-04 | LLM Copilot → Dashboard | API → UI | WebSocket JSON stream | Alerts, predictions, topology changes |
| IF-05 | Floci → All | Infrastructure → Every Layer | AWS SDK calls | S3 storage, DynamoDB records, SQS events |
| IF-06 | Fault Injection → Topology | Test → Network | CLI/Python | Netem delay/loss, BGP flaps, link shutdowns |

> **Build tip:** Mock IF-01 through IF-04 during development. Only connect the full pipeline in Session 10.

### 📅 10-Session Build Schedule

| Session | Role | Build | Files | Definition of Done |
|---------|------|-------|-------|-------------------|
| **S1** | Infra | Environment + Floci | 8 files | `docker compose up` for Floci, `make health-check` passes |
| **S2** | Network | Containerlab topology + FRR configs | 12 files | `sudo containerlab inspect` shows all nodes, BGP/OSPF established |
| **S3** | Network | TRex traffic + Fault injection | 8 files | Traffic flowing, `./fault-inject.sh bgp-flap` causes visible changes |
| **S4** | Telemetry | Telegraf + Prometheus + Kafka + ES | 10 files | Prometheus targets all UP, Kafka topics receiving messages |
| **S5** | ML | Training data + LSTM model | 10 files | `train_lstm.py` completes, eval F1 > 0.80 on validation set |
| **S6** | ML | Prophet + GNN + XGBoost ensemble | 8 files | Ensemble F1 > 0.85, ONNX export passes |
| **S7** | LLM | Ollama + Qwen3-8B GGUF | 6 files | `ollama run airgap-mistral` works offline, prompt template tested |
| **S8** | LLM | ChromaDB + RAG + FastAPI copilot | 10 files | `curl /api/v1/chat` returns structured response, WebSocket connects |
| **S9** | Frontend | NOC Dashboard (3D + anime.js) | 15 files | `npm run dev` shows 3D topology, real-time charts, chat panel |
| **S10** | All | Integration + Validation + Air-Gap | 8 files | All 7 fault scenarios pass, `airgap-verify.sh` ALL PASS |

**Total: ~95 files created across 10 sessions. Each session is 4–6 hours of focused work.**

### 🎯 Official Challenge Phase Mapping

| Official Phase | Our Sessions | Weight |
|----------------|--------------|--------|
| **Phase 1:** Data Generation & Labeling | S2–S4 | — |
| **Phase 2:** Model Training & Validation | S5–S6 | — |
| **Phase 3:** Offline LLM & RAG Integration | S7–S8 | — |
| **Phase 4:** NOC Dashboard & Visualization | S9 | — |
| **Phase 5:** End-to-End Evaluation | S10 | — |
| **Phase 6:** Optimization & Air-Gap Hardening | S10 | — |

### 📂 File Inventory (What Gets Built)

```
Session 1  ├── docker/floci.yml, docker/network.yml, docker/telemetry.yml
            ├── docker/copilot.yml, Makefile, scripts/deploy.sh
            ├── scripts/health-check.sh, scripts/airgap-verify.sh

Session 2  ├── sim/topology.clab.yml, sim/frr/pe1/daemons, sim/frr/pe1/frr.conf
            ├── sim/frr/pe2/*, sim/frr/pe3/*, sim/frr/p1/*, sim/frr/p2/*, sim/frr/p3/*
            ├── sim/frr/ce-a1/*, sim/frr/ce-a2/*, sim/frr/ce-b1/*, sim/frr/ce-b2/*

Session 3  ├── sim/traffic/profiles/*.yaml, sim/traffic/start-traffic.sh
            ├── sim/faults/inject-congestion.sh, sim/faults/inject-bgp-flap.sh
            ├── sim/faults/inject-link-failure.sh, sim/faults/inject-latency.sh
            ├── sim/faults/inject-packet-loss.sh, sim/faults/run-suite.sh

Session 4  ├── telemetry/telegraf/telegraf.conf, telemetry/prometheus/prometheus.yml
            ├── telemetry/prometheus/alerts.yml, telemetry/kafka/create-topics.sh
            ├── telemetry/stream-processor.py, telemetry/elasticsearch/init.sh

Session 5  ├── ml/prepare_dataset.py, ml/features/build_features.py
            ├── ml/features/config.yaml, ml/trainers/train_lstm.py
            ├── ml/evaluate/evaluate_model.py, ml/run-training-scenarios.sh

Session 6  ├── ml/trainers/train_prophet.py, ml/trainers/train_gnn.py
            ├── ml/trainers/train_ensemble.py, ml/trainers/generate_meta_features.py
            ├── ml/export_to_onnx.py, ml/evaluate/run_evaluation.py

Session 7  ├── copilot/llm/Modelfile, copilot/llm/download.sh
            ├── copilot/rag/populate_vector_db.py, copilot/rag/query_vector_db.py

Session 8  ├── copilot/api/main.py, copilot/api/requirements.txt
            ├── copilot/api/context_builder.py, copilot/api/response_formatter.py
            ├── copilot/runbooks/*.md (5+ runbooks)

Session 9  ├── dashboard/package.json, dashboard/tsconfig.json
            ├── dashboard/src/* (15+ React components)
            ├── dashboard/public/*, dashboard/index.html

Session 10 ├── sim/faults/run_validation_suite.sh, data/validation/*
```

---

## 🛠 Tech Stack

### Network Simulation
| Tool | Purpose |
|------|---------|
| [Containerlab](https://containerlab.dev) | Multi-vendor network topology orchestration |
| FRRouting (FRR) | BGP/OSPF dynamic routing on CE/PE/P nodes |
| StrongSwan / WireGuard | IPSec tunnel encryption over MPLS underlay |
| DPDK / TRex | High-performance traffic generation |
| Custom fault-injection scripts | Congestion, route flaps, link failures |

### Telemetry Pipeline
| Tool | Purpose |
|------|---------|
| Telegraf | Metrics collection from simulated devices (SNMP, gNMI) |
| Prometheus | Time-series storage and alerting rules |
| Apache Kafka | Stream buffer for real-time event processing |
| Elasticsearch | Log aggregation and syslog indexing |
| Loki | Lightweight log aggregation (air-gap optimized) |

### Machine Learning & Predictions
| Model | Application |
|-------|-------------|
| **LSTM** | Time-series forecasting for congestion, latency drift, utilization |
| **Prophet** | Seasonal trend decomposition for traffic patterns |
| **Graph Neural Network** | Topology-aware anomaly detection on graph state |
| **Isolation Forest** | Real-time outlier detection on multivariate telemetry |
| **XGBoost Ensemble** | Final classifier fusing all model outputs with confidence scoring |

### Offline LLM & RAG
| Component | Technology |
|-----------|------------|
| **Base LLM** | Qwen3-8B (Q4_K_M, 6.0 GB VRAM — full GPU on RTX 4060) |
| **Fallback** | Qwen3-4B-Thinking (Q5_K_M, 3.9 GB) |
| **Inference** | llama.cpp / Ollama (offline mode) |
| **Vector Store** | ChromaDB (local, no telemetry) |
| **RAG Framework** | LangChain (local-only retrievers) |
| **Embeddings** | all-MiniLM-L6-v2 (local SentenceTransformers) |

### Frontend & Visualization
| Component | Technology |
|-----------|------------|
| **Dashboard Framework** | React 18 + TypeScript |
| **3D Network Visualization** | Three.js / React Three Fiber |
| **Animations** | anime.js |
| **Real-Time Charts** | Apache ECharts / D3.js |
| **Telemetry Overlay** | Grafana (embedded panels) |
| **Styling** | Tailwind CSS + glassmorphism design system |

### Infrastructure (Air-Gapped)
| Tool | Purpose |
|------|---------|
| [Floci](https://github.com/floci-io/floci) | Local AWS emulation (S3, DynamoDB, Lambda, SQS, KMS) |
| Docker Compose | Service orchestration |
| Local Docker Registry | Container image caching (no pull from internet) |
| MinIO | S3-compatible object storage (fallback) |

---

## 🚀 Getting Started

### Prerequisites

- **Linux** (Ubuntu 22.04+ / RHEL 9+ recommended)
- **Docker** 24.0+ with Compose plugin
- **Python** 3.11+
- **Go** 1.22+ (for Containerlab)
- **Make** 4.0+
- **At least 16 GB RAM** (15 GB available on dev machine — will be tight with LLM + Docker)
- **NVIDIA RTX 4060 Laptop** 8 GB VRAM (CUDA 13.3) — Qwen3-8B Q4_K_M fits entirely on GPU (6.0 GB)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/your-team/isro-mpls-copilot.git
cd isro-mpls-copilot

# 2. Launch the air-gapped infrastructure
make up

# 3. Start Floci (local AWS emulation)
docker compose -f docker/floci.yml up -d

# 4. Deploy network simulation
make deploy-topology

# 5. Start telemetry pipeline
make start-telemetry

# 6. Train/load predictive models
make train-models

# 7. Launch the LLM copilot
make start-copilot

# 8. Open the NOC dashboard
make dashboard
# → http://localhost:3000
```

### Verification

```bash
# Check all services are healthy
make health-check

# Run fault injection scenarios
make inject-fault fault=bgp-flap
make inject-fault fault=congestion
make inject-fault fault=link-failure

# View predictions
make query-copilot "What is likely to fail next?"
```

---

## 📁 Project Structure

```
├── README.md                 # This file
├── SR.md                     # 🔒 Secrets & rules (gitignored — see .gitignore)
├── .gitignore                # Git exclusion rules
├── .opencode/
│   └── rules.md              # OpenCode behavioural rules (pre-push guard)
│
├── info/                     # 📚 Challenge documentation
│   ├── flow.md               # Software & technology flowcharts
│   ├── frontend.md           # Frontend architecture (3D · anime.js)
│   ├── resources.md          # All resources, APIs, data sources
│   ├── main.md               # Main project deep-dive
│   └── build.md              # Step-by-step build guide
│
├── sim/                      # 🌐 Network simulation
│   ├── topology.clab.yml     # Containerlab topology definition
│   ├── frr/                  # FRRouting configs per node
│   ├── ipsec/                # IPSec tunnel configurations
│   ├── traffic/              # TRex traffic generation profiles
│   └── faults/               # Fault injection scripts
│
├── telemetry/                # 📊 Telemetry pipeline
│   ├── telegraf/             # Telegraf configs + plugins
│   ├── prometheus/           # Prometheus rules + alerts
│   ├── kafka/                # Kafka stream configs
│   └── elasticsearch/        # ES index templates
│
├── ml/                       # 🧠 Predictive models
│   ├── models/               # Trained model artifacts
│   ├── trainers/             # Training scripts (LSTM, Prophet, GNN)
│   ├── features/             # Feature engineering pipeline
│   └── evaluation/           # Model evaluation scripts
│
├── copilot/                  # 🤖 Offline LLM Copilot
│   ├── llm/                  # Quantized model + runtime config
│   ├── rag/                  # RAG pipeline (ChromaDB, LangChain)
│   ├── runbooks/             # Internal runbook collection
│   └── api/                  # Copilot REST API (FastAPI)
│
├── dashboard/                # 🖥️ NOC Dashboard
│   ├── src/                  # React + TypeScript source
│   ├── components/           # 3D network viz, charts, overlays
│   └── public/               # Static assets
│
├── floci/                    # ☁️ Local AWS Emulation
│   ├── compose.yml           # Floci Docker Compose
│   ├── init-scripts/         # Floci init (S3 buckets, SQS queues, etc.)
│   └── lambda/               # Lambda functions for automation
│
├── docker/                   # 🐳 Docker & infrastructure
│   ├── floci.yml             # Floci service definition
│   ├── telemetry.yml         # Telemetry stack compose
│   └── copilot.yml           # LLM copilot service
│
├── scripts/                  # 🔧 Utility scripts
│   ├── deploy.sh             # Full deployment automation
│   ├── health-check.sh       # Service health verification
│   ├── fault-inject.sh       # Fault injection executor
│   └── airgap-verify.sh      # Air-gap integrity validator
│
├── Makefile                  # Build orchestration
└── docs/                     # 📖 Additional documentation
    ├── architecture.md
    ├── api.md
    └── scenarios.md
```

---

## 📚 Documentation

All in-depth documentation is in the [`info/`](./info/) directory:

| File | Description |
|------|-------------|
| [`info/flow.md`](./info/flow.md) | Detailed flowcharts — telemetry pipeline, ML training, copilot inference, fault injection |
| [`info/frontend.md`](./info/frontend.md) | NOC Dashboard design — 3D network viz with Three.js, anime.js micro-interactions |
| [`info/resources.md`](./info/resources.md) | Comprehensive resource index — tools, libraries, datasets, references |
| [`info/main.md`](./info/main.md) | Deep dive into the main system design and components |
| [`info/build.md`](./info/build.md) | Step-by-step build instructions from zero to deployed system |

---

## 🔐 Security & Air-Gap Compliance

This project is designed from the ground up for **air-gapped, regulated, and government environments**.

### Air-Gap Verification

| Check | Status | Method |
|-------|--------|--------|
| Zero outbound DNS at runtime | ✅ | `airgap-verify.sh` monitors DNS queries |
| No cloud API calls | ✅ | All API endpoints local (Floci, Docker, internal) |
| Offline model inference | ✅ | llama.cpp with zero telemetry |
| Local package cache | ✅ | `docker/` pre-bundled images, pip cache |
| No telemetry exfiltration | ✅ | All logs stay within the boundary |

### Security Controls

- **Role-based access** on the NOC dashboard (admin, operator, read-only)
- **All secrets** in `SR.md` (gitignored) — never in source code
- **Local KMS** via Floci for key management within the air gap
- **Audit logging** of all operator copilot queries
- **Model input sanitization** — the RAG pipeline validates context before LLM inference

### SR.md (Secrets & Rules)

Sensitive credentials, API keys, and operational rules are stored in [`SR.md`](./SR.md), which is **excluded from version control** via `.gitignore`. See the file for:

- Local infrastructure passwords and keys
- Floci credentials
- Team-specific configuration
- Operational rules (including the pre-push prompt requirement)

---

## 📊 Evaluation Criteria Mapping

| Criterion | Weight | How We Address It |
|-----------|--------|-------------------|
| **Technical Merit** | 35% | Multi-model ensemble (LSTM + Prophet + GNN + XGBoost) with configurable lead-time targets; fault injection ground-truth validation |
| **Copilot Effectiveness** | 35% | Qwen3-8B (Q4_K_M, full GPU 6.0 GB on RTX 4060) with local RAG; structured responses (prediction, confidence, root cause, scope, action); human-validated on 10+ scenarios |
| **Security & Offline Compliance** | 20% | Verifiable air-gap integrity scanner; zero cloud dependencies; local Floci emulation; all model artifacts bundled |
| **Documentation Quality** | 10% | Comprehensive README, `info/` docs, architecture diagrams, build guide, runbooks |

---

## 👤 Solo Developer

> **Built by a solo developer — wearing all four hats across 10 sessions.**

| Role (Hat) | When | Deliverables |
|------------|------|--------------|
| 🌐 **Network Engineer** | Sessions 1–3 | Containerlab topology, FRR (BGP/OSPF/MPLS), IPSec tunnels, TRex traffic, fault injection |
| 📊 **Data/ML Engineer** | Sessions 4–6 | Telegraf/Prometheus/Kafka pipeline, LSTM + Prophet + GNN models, XGBoost ensemble |
| 🤖 **LLM/RAG Engineer** | Sessions 7–8 | Ollama + Qwen3-8B (quantized), ChromaDB vector store, LangChain RAG, FastAPI copilot |
| 🎨 **Frontend + Infra** | Sessions 9–10 | NOC Dashboard (React + Three.js + anime.js + ECharts), Floci integration, air-gap validation |

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ for ISRO Bharatiya Antariksh Hackathon 2026 — Challenge 13</sub>
  <br>
  <sub>Powered by <a href="https://github.com/floci-io/floci">Floci</a> · Containerlab · Qwen3-8B · Three.js</sub>
</div>
