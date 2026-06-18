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
3. ✅ Runs a fully offline quantized LLM (Mistral 7B / LLaMA 3) with RAG over internal runbooks
4. ✅ Answers three critical questions in real time:
   - **Q1:** *What is likely to fail next — and when?*
   - **Q2:** *Why is risk elevated — which signals contributed?*
   - **Q3:** *What corrective action should be taken before SLA or security impact occurs?*

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔮 **Predictive Fault Analytics** | LSTM + Prophet + graph-based anomaly detection with configurable lead-time targets |
| 🤖 **Offline LLM Copilot** | Quantized Mistral 7B / LLaMA 3 with local RAG — zero cloud dependency |
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
│  ┌──────────┐                      │  Mistral 7B · RAG · QA   │   │
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
| **Base LLM** | Mistral 7B Instruct v0.3 (4-bit GPTQ quantized) |
| **Fallback** | LLaMA 3 8B / Phi-3-mini (GGUF quantized) |
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
- **At least 32 GB RAM** (64 GB recommended for LLM + simulation)
- **NVIDIA GPU** with 8 GB+ VRAM (optional, for LLM acceleration)

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
| **Copilot Effectiveness** | 35% | Quantized Mistral 7B with local RAG; structured responses (prediction, confidence, root cause, scope, action); human-validated on 10+ scenarios |
| **Security & Offline Compliance** | 20% | Verifiable air-gap integrity scanner; zero cloud dependencies; local Floci emulation; all model artifacts bundled |
| **Documentation Quality** | 10% | Comprehensive README, `info/` docs, architecture diagrams, build guide, runbooks |

---

## 👥 Team

> *Your team name — ISRO BAH 2026*

| Role | Responsibility |
|------|----------------|
| **Network Architect** | Containerlab topology, FRR configs, fault injection |
| **ML Engineer** | Predictive models (LSTM, Prophet, GNN), feature pipeline |
| **LLM / RAG Engineer** | Quantized model deployment, ChromaDB, LangChain pipeline |
| **Full-Stack Developer** | NOC Dashboard (React, Three.js, anime.js, Grafana) |
| **DevOps / Security** | Floci integration, air-gap verification, CI/CD |

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ for ISRO Bharatiya Antariksh Hackathon 2026 — Challenge 13</sub>
  <br>
  <sub>Powered by <a href="https://github.com/floci-io/floci">Floci</a> · Containerlab · Mistral 7B · Three.js</sub>
</div>
