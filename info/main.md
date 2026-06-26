# Main Architecture — PS13

## Air-Gapped Predictive Copilot for Secure MPLS Operations

An AI-powered NOC copilot that simulates a multi-site enterprise MPLS/SD-WAN network, streams real-time telemetry, predicts network failures using an ensemble of ML models, and provides natural-language diagnostic assistance via an offline LLM with RAG over 50+ internal runbook documents — all running air-gapped on a single RTX 4060 laptop.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PS13 NOC Dashboard                              │
│                                                                         │
│  ┌──────────────┐  ┌────────────────────┐  ┌──────────────────────┐    │
│  │  Left Panel   │  │   Center Panel      │  │   Right Panel        │    │
│  │  Dashboard    │  │   IndiaMap          │  │   AI Chat            │    │
│  │  Network Ovw  │  │   CityOrbitView     │  │   (Ollama Qwen3-8B   │    │
│  │  ML Models    │  │   DeviceInspector   │  │    + RAG)            │    │
│  │  Alert Feed   │  │                     │  │                      │    │
│  └──────┬───────┘  └─────────┬───────────┘  └──────────┬───────────┘    │
│         │                    │                          │               │
│         └────────────┬───────┴─────────────┬────────────┘               │
│                      ▼                     ▼                            │
│             ┌──────────────┐     ┌──────────────────┐                   │
│             │   Express    │     │     FastAPI      │                   │
│             │   :3000      │     │     :8000        │                   │
│             │  REST API    │     │  ML Inference    │                   │
│             │  SPA Serve   │     │  ChromaDB RAG    │                   │
│             └──────┬───────┘     └────────┬─────────┘                   │
│                    │                      │                            │
│                    ▼                      ▼                            │
│             ┌──────────────┐     ┌──────────────────┐                   │
│             │   Ollama     │     │  GPU (RTX 4060)  │                   │
│             │   :11434     │     │  CUDA 13.3       │                   │
│             │  qwen3:8b    │     │  8GB VRAM        │                   │
│             └──────────────┘     └──────────────────┘                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3-Terminal Architecture

### Terminal 1 (port 11434) — Ollama LLM
- **Model**: qwen3:8b (8.2B params, Q4_K_M, 5.2GB)
- **Purpose**: Natural-language network diagnostics
- **Acceleration**: NVIDIA CUDA 13.3, RTX 4060 8GB VRAM
- **Integration**: FastAPI calls via Ollama Python SDK

### Terminal 2 (port 8000) — FastAPI + RAG + ML
- **Server**: `uvicorn noc_copilot:app --host 0.0.0.0 --port 8000`
- **RAG**: ChromaDB (7,920 indexed runbook docs)
- **ML Models Loaded**:
  - XGBoost — fault type classification
  - Isolation Forest — anomaly detection
  - Autoencoder — reconstruction error
  - Prophet — trend/seasonality decomposition
  - TTI Regressor — time-to-incident prediction
- **ML Models Offline (expected)**:
  - LSTM — time-series forecasting (requires TensorFlow)
  - GNN — failure propagation (requires PyTorch Geometric)
- **Health Check**: `GET /api/health` — returns LLM latency, RAG doc count, ML model status

### Terminal 3 (port 3000) — Express + React SPA
- **Server**: Node.js Express serving built React app + REST API
- **React App**: Vite + TypeScript + Tailwind
- **14 API Endpoints**: cities, devices, alerts, analytics, system status, events, chat, reset
- **3D Visuals**: Three.js (via @react-three/fiber) — Starfield background, CityOrbitView orbital rings, device models

---

## Dashboard Layout

| Panel | Component | Content |
|-------|-----------|---------|
| **Left** (320px) | LeftPanel.tsx | Network Overview (4 cities, device counts), Live Alerts (pinned sticky, scrollable feed), ML Model Ensemble (5 loaded models with status) |
| **Center** (1fr) | State-machine view | IndiaMap (SVG, clickable cities) → CityOrbitView (device nodes, orbital rings, connection paths) → DeviceInspector (health metrics, CPU/memory bars, fault triggers) |
| **Right** (340px) | ChatTab.tsx | AI Chat with Ollama LLM (markdown formatting, timestamps, auto-focus) |
| **Bottom** (hidden on hover) | ControlBar.tsx | Trigger fault (city/device/type selector), Random Burst, Reset Dashboard, ML Predict |

---

## Data Flow

```
User clicks city on IndiaMap
  → selectCity(id) in NocContext
  → App.tsx sets centerView = "orbit", shows CityOrbitView for that city
  → User clicks device node (e.g., P1)
  → selectDevice("P1") in NocContext
  → App.tsx sets centerView = "device", shows DeviceInspector
  → DeviceInspector fetches GET /api/devices/{cityId}_{deviceName}/health

User types chat message
  → ChatTab sends POST /api/chat { message, alerts }
  → Express proxies to FastAPI /api/chat
  → FastAPI queries Ollama qwen3:8b with RAG context
  → Response streamed back → rendered in ChatTab with markdown formatting

ControlBar trigger fault
  → POST /api/events/trigger { cityId, deviceName, type }
  → Express creates alert, broadcasts to NocContext
  → Alert appears in LeftPanel, toast notification shown

Header status dots
  → GET /api/system/status every 30s
  → Probes: Ollama:11434, FastAPI:8000, Network, Docker
```

---

## API Endpoints (Express :3000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/cities | List all simulated cities |
| GET | /api/cities/:cityId/devices | Devices for a city |
| GET | /api/alerts | All alerts (sorted: pinned + timestamp) |
| GET | /api/alerts/summary | Alert summary stats |
| GET | /api/devices/:deviceId | Device details |
| GET | /api/devices/:deviceId/health | Health metrics (CPU, memory, uptime) |
| GET | /api/system/status | Service health probe (Ollama, FastAPI, Docker) |
| GET | /api/analytics | Aggregated dashboard analytics |
| POST | /api/events/trigger | Inject fault (cityId, deviceName, type) |
| POST | /api/events/random-burst | Inject 4 random faults |
| PATCH | /api/alerts/:id/pin | Toggle alert pin |
| DELETE | /api/alerts/:id | Delete alert |
| POST | /api/chat | Chat with Ollama via FastAPI |
| POST | /api/dashboard/reset | Reset to initial state |

---

## Fault Scenarios (7 types)

| Type | Severity | Title Pattern |
|------|----------|---------------|
| latency | warning | Latency Spike |
| packet_loss | warning | Packet Loss |
| congestion | critical | Link Congestion |
| bgp_flap | critical | BGP Session Flap |
| ospf_issue | critical | OSPF Neighbor Down |
| link_down | critical | Link Down |
| route_leak | critical | Route Leak |

---

## Infrastructure

| Service | Role | Technology |
|---------|------|-----------|
| Ollama | LLM runtime | Local GPU (RTX 4060) |
| ChromaDB | Vector store for RAG | Local persistent |
| FastAPI | ML + RAG inference | Uvicorn + Python 3.11 |
| Express | SPA server + REST API | Node.js + tsx |
| React | Frontend SPA | Vite + TypeScript + Tailwind |
| Three.js | 3D visualizations | @react-three/fiber + drei |
| Docker | System status probe | docker info |

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

## North Star — Q1 / Q2 / Q3

### Q1 — Network Simulation
> *"Does the simulated network behave like a real enterprise MPLS/SD-WAN?"*

The simulation (in-memory Express state + reactive UI) must realistically model 4-city MPLS topology with 2 P routers, 2 PE routers, and 2 E routers per city, support fault injection, and display real-time health metrics.

### Q2 — ML Prediction & LLM Copilot
> *"Can the system predict failures and explain them in plain language?"*

The ML ensemble must detect anomalies, forecast utilization, and predict time-to-incident. The Ollama LLM with RAG must produce structured diagnostic responses that a NOC operator can act on immediately.

### Q3 — Air-Gap & Automation
> *"Does everything work without touching the internet?"*

Ollama, ChromaDB, FastAPI, and Express all run locally. Zero cloud dependencies. The entire system is self-contained on the RTX 4060 laptop.

---

*Air-gapped by design. No cloud dependency. All data stays local.*
