# Build Plan — PS13

Team build of the Air-Gapped Predictive Copilot for Secure MPLS Operations. This document reflects the **current completed build state**.

---

## Build Phases (Completed)

### Phase 1: Backend Services
- Express server with in-memory state (4 cities, 16 devices, alert management)
- 14 REST API endpoints implemented and verified
- FastAPI service (noc_copilot.py) with 5 ML models loaded
- ChromaDB vector store with 7,920 indexed runbook documents
- Ollama qwen3:8b pulled and running on GPU

### Phase 2: Frontend Core
- Vite + React + TypeScript + Tailwind setup
- NocContext state management (Context API)
- 3-panel dashboard layout
- IndiaMap with real SVG outline + geo-projected city coordinates
- State-machine center view (map → orbit → device)
- Data flow: all buttons trigger real API endpoints

### Phase 3: UI Polish
- Animejs entrance animations (connection lines, city nodes, labels)
- Framer Motion view transitions (AnimatePresence)
- Boot loading sequence with typewriter effect
- Toast notifications (auto-dismiss 4s)
- "Updated Xs ago" timestamps
- Health bar shimmer effect
- Chat markdown formatting + timestamps + auto-focus
- Pin/delete icons on alerts
- Re-scan connectors (Header)
- Reset Dashboard (ControlBar)

### Phase 4: Run Scripts
- ps13.sh — tmux 3-pane session (Ollama, FastAPI, Express)
- ps13-ollama.sh — Terminal 1
- ps13-fastapi.sh — Terminal 2
- ps13-frontend.sh — Terminal 3
- stop.sh — Clean shutdown all services

### Phase 5: Documentation
- README.md with project structure, setup, architecture
- info/main.md — architecture overview
- info/flow.md — data flow sequences
- info/frontend.md — frontend architecture
- info/build.md — build plan (this file)
- Info/T1/T2/T3 — terminal documentation

---

## Current Project Structure

```
/home/ego/Documents/ISRO2026/
├── index.html                     # Entry point (title: PS13)
├── package.json                   # Dependencies
├── vite.config.ts                 # Vite configuration
├── tsconfig.json                  # TypeScript config
├── tailwind.config.js             # Tailwind CSS config
├── postcss.config.js              # PostCSS config
├── server.ts                      # Express server (REST API + SPA serve)
├── noc_copilot.py                 # FastAPI server (ML + RAG + LLM)
├── ps13.sh                        # 3-terminal tmux launcher
├── ps13-ollama.sh                 # Terminal 1: Ollama
├── ps13-fastapi.sh                # Terminal 2: FastAPI
├── ps13-frontend.sh               # Terminal 3: Express+React
├── stop.sh                        # Service shutdown
├── README.md
├── info/                          # Documentation
│   ├── main.md, flow.md, frontend.md, build.md
│   ├── T1.md, T2.md, T3.md
│   ├── frontend1.md, frontend2.md (legacy)
│   ├── problem-statement.md, problem-statement-exact.md
│   ├── resources.md, learn.md, future.md
│   └── SR.md (gitignored)
├── src/                           # React app
│   ├── App.tsx                    # Root component (layout, routing state)
│   ├── main.tsx                   # React entry
│   ├── index.css                  # Tailwind + animations + theme
│   ├── context/NocContext.tsx      # Global state
│   ├── services/api.ts            # Typed API client
│   ├── types.ts                   # TypeScript types
│   └── components/
│       ├── Header.tsx             # Top bar with status dots
│       ├── LeftPanel.tsx          # Dashboard + alerts
│       ├── ControlBar.tsx         # Bottom trigger bar
│       ├── ChatTab.tsx            # AI chat panel
│       ├── Starfield.tsx          # CSS star background
│       └── shared/
│           ├── IndiaMap.tsx        # SVG India with city markers
│           ├── CityOrbitView.tsx   # 3D R3F orbital scene
│           ├── DeviceInspector.tsx # Device health details
│           └── AnalyticsCard.tsx   # Reusable stat card
├── ml/                            # ML models + data
│   └── chroma_db/                 # ChromaDB persistent storage
└── dist/                          # Built frontend (vite output)
```

---

## Running the Project

```bash
# Quick start (3 terminals via tmux)
./ps13.sh

# Or manual start:
./ps13-ollama.sh     # Terminal 1
./ps13-fastapi.sh    # Terminal 2
./ps13-frontend.sh   # Terminal 3

# Stop all services
./stop.sh

# Access dashboard
# http://localhost:3000
```

---

## Verification Checklist

| Check | Command | Expected |
|-------|---------|----------|
| Express running | `curl -s localhost:3000` | HTML page |
| FastAPI running | `curl -s localhost:8000/api/health` | JSON health |
| Ollama running | `curl -s localhost:11434/api/tags` | Model list |
| Cities endpoint | `curl -s localhost:3000/api/cities` | 4 cities |
| Alerts empty | `curl -s localhost:3000/api/alerts` | `[]` |
| System status | `curl -s localhost:3000/api/system/status` | All true |
| Frontend build | `npx vite build` | 1680+ modules, <2s |

---

## Tech Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + TypeScript + Tailwind |
| 3D Graphics | Three.js (@react-three/fiber + drei) |
| Animations | anime.js v4 + Framer Motion |
| Icons | Lucide React |
| Backend API | Express + Node.js (tsx) |
| ML + RAG | FastAPI + Python 3.11 |
| LLM | Ollama + qwen3:8b |
| Vector Store | ChromaDB |
| GPU | CUDA 13.3 / RTX 4060 |

---

## Evaluation Criteria

| Component | Weight | Criteria |
|-----------|--------|----------|
| **Network Simulation** | 35% | 4-city MPLS topology, 16 device roles, 7 fault scenarios inject and display |
| **ML Prediction** | 35% | 5 models loaded and inferring, predictions displayed in dashboard |
| **LLM Copilot** | (included in ML) | Structured diagnostic responses, RAG-augmented, response < 15s |
| **NOC Workflow** | 10% | Alert correlation, pin/delete, toast notification, incident lifecycle |
| **Air-Gap Integrity** | 10% | All services local, zero cloud dependencies |
| **Documentation** | 10% | All info/ docs maintained, run scripts documented |

---

## Future Work

- Re-enable LSTM + GNN models (TensorFlow + PyTorch Geometric)
- Add WebSocket for live telemetry streaming
- Persistent alert history (SQLite)
- Real device integration (SSH to network gear)
- Multi-user session support
- Time-series charts (ECharts or Recharts)
