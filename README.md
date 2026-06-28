# Air-Gapped Predictive Copilot for Secure MPLS Operations

**ISRO 2026 — Team Cyber Assassins**

A team-developed, air-gapped NOC copilot that simulates a multi-site enterprise MPLS/SD-WAN network, streams real-time telemetry, predicts failures using an ensemble of ML models, and provides natural-language diagnostic assistance via an offline LLM with Retrieval-Augmented Generation (RAG).

No cloud dependency. No internet required at runtime. All inference, storage, and orchestration runs locally on a single RTX 4060 laptop.

---

## Architecture (3-Terminal)

```
┌──────────────────────────────────────────────────────────────────────┐
│              TERMINAL 1: Ollama LLM (port 11434)                     │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  ollama serve                                                  │  │
│  │  • Model: qwen3:8b (8.2B params, Q4_K_M, 5.2GB)              │  │
│  │  • GPU: NVIDIA CUDA 13.3, RTX 4060 (8GB VRAM)                 │  │
│  └────────────────────────────┬───────────────────────────────────┘  │
│                               │ ollama Python SDK                     │
└───────────────────────────────┼───────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│           TERMINAL 2: FastAPI + RAG + ML (port 8000)                 │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  uvicorn noc_copilot:app                                       │  │
│  │  • ChromaDB RAG — 7,920 indexed runbook docs                  │  │
│  │  • ML Models: XGBoost, Isolation Forest, Autoencoder,          │  │
│  │    Prophet, TTI Regressor                                      │  │
│  │  • Health check: GET /api/health                               │  │
│  │  • Chat proxy: POST /api/chat → Ollama + RAG context           │  │
│  └────────────────────────────┬───────────────────────────────────┘  │
│                               │ HTTP (predictions, chat)              │
└───────────────────────────────┼───────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│          TERMINAL 3: Express + React Dashboard (port 3000)           │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  npx tsx server.ts + npx vite build                            │  │
│  │  • Single-page React dashboard (Vite + TypeScript + Tailwind)  │  │
│  │  • 3-panel layout: Alerts/Dashboard | IndiaMap | AI Chat       │  │
│  │  • 14 REST API endpoints (cities, devices, alerts, events...)  │  │
│  │  • 3D visualizations (Three.js R3F — Starfield, OrbitViews)    │  │
│  │  • Anime.js entrance animations on IndiaMap                    │  │
│  │  • Framer Motion view transitions + toast system               │  │
│  │  • State-machine center view: Map → Orbit → Device             │  │
│  └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Features

### NOC Dashboard
- **India Map**: Interactive SVG map with clickable city markers (BLR, DEL, BOM, MAA) with geo-projected coordinates
- **City Orbital View**: 3D R3F scene with device nodes, orbital rings, connection paths with continuous data-flow animation
- **Device Inspector**: Health metrics (CPU, memory, uptime) with shimmer progress bars
- **Alert Feed**: Pinned alerts always visible, scrollable non-pinned list, pin/delete icons
- **AI Chat**: RAG-augmented Ollama Qwen3-8B with markdown-formatted responses, typing indicators, timestamps

### ML Ensemble
- **XGBoost**: Fault type classification from telemetry signature
- **Isolation Forest**: Real-time anomaly detection on metric streams
- **Autoencoder**: Reconstruction-error based anomaly detection
- **Prophet**: Trend/seasonality decomposition of network KPIs
- **TTI Regressor**: Time-to-incident prediction for proactive maintenance

### Fault Simulation (7 Types)
| Type | Severity | Description |
|------|----------|-------------|
| latency | warning | Latency spike on device link |
| packet_loss | warning | Packet loss detected |
| congestion | critical | Link congestion > 90% utilization |
| bgp_flap | critical | BGP session oscillating |
| ospf_issue | critical | OSPF neighbor down |
| link_down | critical | Physical link down |
| route_leak | critical | Route advertisement leak |

### UI Polish
- Boot loading sequence (5-step typewriter with [OK] markers)
- Anime.js entrance animations (connection line draw, city node bounce, label slide)
- Toast notifications (auto-dismiss after 4s)
- "Updated Xs ago" live timestamps
- Health bar shimmer effect
- Chat message markdown formatting + timestamps
- Framer Motion AnimatePresence view transitions

---

## Project Structure

```
ISRO2026/
├── index.html                  # Entry point (title: PS13)
├── package.json                # Node dependencies
├── vite.config.ts              # Vite bundler config
├── tsconfig.json               # TypeScript config
├── tailwind.config.js          # Tailwind CSS config
├── postcss.config.js           # PostCSS config
├── server.ts                   # Express server (REST API + SPA)
├── noc_copilot.py              # FastAPI server (ML + RAG + LLM)
├── stop.sh                     # Stop all services
├── ps13.sh                     # 3-terminal tmux launcher
├── ps13-ollama.sh              # Terminal 1 script
├── ps13-fastapi.sh             # Terminal 2 script
├── ps13-frontend.sh            # Terminal 3 script
├── README.md
├── info/                       # Project documentation
│   ├── main.md                 # Architecture overview
│   ├── flow.md                 # Data flow sequences
│   ├── frontend.md             # Frontend architecture
│   ├── build.md                # Build plan + project structure
│   ├── T1.md                   # Ollama terminal docs
│   ├── T2.md                   # FastAPI terminal docs
│   ├── T3.md                   # Express+React terminal docs
│   ├── frontend1.md            # Legacy reference
│   ├── frontend2.md            # Legacy reference
│   ├── problem-statement.md    # Problem statement
│   ├── problem-statement-exact.md
│   ├── resources.md            # Stack references
│   ├── learn.md                # Learning path
│   ├── future.md               # Future roadmap
│   └── SR.md                   # (gitignored)
├── src/                        # React application
│   ├── App.tsx                 # Root component + layout
│   ├── main.tsx                # React entry point
│   ├── index.css               # Tailwind + animations + theme
│   ├── context/
│   │   └── NocContext.tsx      # Global state (Context API)
│   ├── services/
│   │   └── api.ts              # Typed REST API client
│   ├── types.ts                # TypeScript interfaces
│   └── components/
│       ├── Header.tsx          # Top bar (logo, status dots)
│       ├── LeftPanel.tsx       # Dashboard + alert feed
│       ├── ControlBar.tsx      # Bottom trigger bar
│       ├── ChatTab.tsx         # AI chat panel
│       ├── Starfield.tsx       # CSS star background
│       └── shared/
│           ├── IndiaMap.tsx     # SVG India map (clickable)
│           ├── CityOrbitView.tsx# 3D orbital scene (R3F)
│           ├── DeviceInspector.tsx # Device health
│           └── AnalyticsCard.tsx   # Stat card component
├── ml/                         # ML models + data
│   └── chroma_db/              # ChromaDB persistent vector store
└── dist/                       # Built frontend (vite output)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + TypeScript + Tailwind CSS |
| 3D Graphics | Three.js (@react-three/fiber + drei) |
| Animations | anime.js v4 + Framer Motion |
| Icons | Lucide React |
| Backend API | Express + Node.js (tsx) |
| ML + RAG | FastAPI + Python 3.11 |
| LLM | Ollama + qwen3:8b |
| Vector Store | ChromaDB |
| GPU | CUDA 13.3 / RTX 4060 |

---

## Hardware

| Component | Spec |
|-----------|------|
| GPU | NVIDIA RTX 4060 (8GB VRAM) |
| CPU | AMD Ryzen 9 8945HS (8 cores / 16 threads) |
| RAM | 15 GB DDR5 |
| Storage | Local NVMe SSD |
| Network | No internet required at runtime |

---

## Quick Start

### Prerequisites
- Node.js 20+
- Python 3.11+
- Ollama (qwen3:8b model pulled)
- tmux (recommended)

### 3-Terminal Run

```bash
# Quick start (all 3 terminals via tmux)
./ps13.sh

# Or manual:
./ps13-ollama.sh      # Terminal 1: Ollama on :11434
./ps13-fastapi.sh     # Terminal 2: FastAPI on :8000
./ps13-frontend.sh    # Terminal 3: Express on :3000
```

Then open **http://localhost:3000** in Firefox.

### Stop All Services

```bash
./stop.sh
```

### Verification

```bash
curl -s localhost:3000/api/cities        # 4 cities
curl -s localhost:3000/api/alerts         # [] (empty, fresh start)
curl -s localhost:3000/api/system/status  # All services green
curl -s localhost:8000/api/health         # FastAPI health
```

---

## Status

**Deployment: Complete. All services running.**

- ✅ Ollama qwen3:8b (GPU, 5.2GB, 8.2B params)
- ✅ FastAPI + ChromaDB RAG (7,920 docs indexed)
- ✅ Express + React SPA (14 API endpoints)
- ✅ 5 ML models loaded (XGBoost, IsoForest, Autoencoder, Prophet, TTI)
- ✅ IndiaMap with real SVG outline + geo-projected cities
- ✅ 3D orbital views (CityOrbitView, Starfield)
- ✅ Anime.js entrance animations
- ✅ Framer Motion view transitions + toast system
- ✅ Fault simulation (7 types, configurable city/device)
- ✅ Alert management (pin, delete, pin-sticky layout)
- ✅ AI Chat with markdown formatting
- ✅ tmux 3-pane launcher (ps13.sh)
- ✅ stop.sh clean shutdown
- ✅ All 15+ hardcoded value fixes applied (dynamic city/device names)
- ✅ Build verification (vite build — 1680+ modules, ~2s)

**Known Issues:**
- LSTM + GNN models offline (require TensorFlow + PyTorch Geometric)
- Server must be started with `./ps13-frontend.sh` or `nohup` (persistent shell)

---

## Documentation

| Document | Content |
|----------|---------|
| `info/main.md` | Architecture overview |
| `info/flow.md` | Data flow sequences |
| `info/frontend.md` | Frontend architecture |
| `info/build.md` | Build plan + project structure |
| `info/T1.md` | Ollama terminal |
| `info/T2.md` | FastAPI terminal |
| `info/T3.md` | Express terminal |
| `info/resources.md` | Stack references |
| `info/learn.md` | Learning path |
| `info/future.md` | Future roadmap |
| `info/problem-statement.md` | Problem statement |
| `info/frontend1.md` | Legacy (1st UI plan) |
| `info/frontend2.md` | Legacy (2nd UI plan) |

---

## Team

**Cyber Assassins** — ISRO 2026

| Role | Member | Contribution |
|------|--------|-------------|
| **Leader + Backend + Design** | Priyanka Meenkeri | Backend architecture, dashboard design, system integration |
| **Frontend + APIs** | Dontamsetti Tanuhya | React/Three.js frontend, REST API endpoints |
| **AI + LLM + RAG** | Shree Raksha | ML model ensemble, Ollama LLM, ChromaDB RAG pipeline |
| **Backend + Deploy + Polish** | Aditya Gowda | Deployment, server orchestration, UI polish, debugging |

*Team-developed. Air-gapped by design. No cloud dependency.*
