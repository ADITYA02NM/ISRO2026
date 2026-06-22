# ISRO BAH 2026 — Challenge 13 (Devices UI + Dashboard UI)

> **Team Cyber Assassins** (4 members: Solo Developer — same guy, 4 times ☠️)

A dual-3D-frontend satellite ground control system with real-time telemetry, fault injection, lockdown isolation, runbook automation, and an AI copilot powered by local LLMs (Qwen3-8B / Qwen3-4B-Thinking on Ollama).

---

##  Architecture — 3 Terminal Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Terminal 1 : Devices UI (5173)    │  Terminal 3 : Dashboard UI (5174) │
│  ┌───────────────────┐             │  ┌───────────────────┐            │
│  │  React + Vite     │             │  │  React + Vite     │            │
│  │  + R3F + drei     │             │  │  + R3F + drei     │            │
│  │  + Three.js       │             │  │  + Three.js       │            │
│  │  + Anime.js       │             │  │  + Anime.js       │            │
│  │                   │             │  │  + ECharts        │            │
│  │  3D NOC Room      │             │  │  3D Room +        │            │
│  │  Interactive      │             │  │  Analytics        │            │
│  │  Devices          │             │  │  Overlays         │            │
│  │  Hover Info       │             │  │  Alert Feed       │            │
│  │  Fault Injection  │             │  │  Copilot Q&A      │            │
│  │  Lockdown Device  │             │  │  Lockdown/SendHelp│            │
│  └────────┬──────────┘             │  └────────┬──────────┘            │
│           │ REST                          WebSocket │                   │
│           │ (commands)                    (push)    │                   │
│           ▼                                         ▼                   │
│  ┌──────────────────────────────────────────────────────┐              │
│  │  Terminal 2 : Backend (8000)                         │              │
│  │  FastAPI + WebSocket + ML/LLM                        │              │
│  │  Qwen3-8B (primary) / Qwen3-4B-Thinking (fallback)  │              │
│  │  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │              │
│  │  │ REST API │  │WS Server│  │ LLM Orchestrator  │  │              │
│  │  │ CRUD     │  │Push     │  │ Fault Analysis     │  │              │
│  │  │ Commands │  │Telemetry│  │ Runbook Generation │  │              │
│  │  │ Config   │  │Alerts   │  │ Anomaly Detection  │  │              │
│  │  └──────────┘  └──────────┘  └───────────────────┘  │              │
│  └──────────────────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────────────┘
         Data Paths:
         ───────────
         REST    (Devices UI → Backend) ── commands, queries, config
         WebSocket (Backend → Dashboard UI) ── telemetry push, alerts, status
```

**Two frontends, one backend, three terminals.** Both UIs are **strictly 3D** — built with React Three Fiber + drei + Three.js. No flat/2D fallback anywhere.

---

##  Tech Stack

| Layer | Technology | Version / Notes |
|-------|-----------|----------------|
| **Frontend 1** (Devices UI) | React + Vite + R3F + drei + Three.js | Port 5173 |
| **Frontend 2** (Dashboard UI) | React + Vite + R3F + drei + Three.js + ECharts | Port 5174 |
| **UI Animation** | Anime.js | v4.4.1 (ESM: `import { animate } from 'animejs'`) |
| **Backend** | FastAPI + Uvicorn + WebSocket | Port 8000 |
| **ML / LLM** | Qwen3-8B (primary) + Qwen3-4B-Thinking (fallback) | Ollama local |
| **Infrastructure** | floci.io (local AWS emulation) | No cloud dependency |
| **Font** | Inter (sans-serif), JetBrains Mono (code/monitor) | Google Fonts |
| **Package Manager** | npm | |

---

## ✨ Features

###  ️ Devices UI (Terminal 1)
- **3D NOC Room** — full R3F/drei/Three.js scene with geometric device models
- **Hover Info Panel** — anime.js animated overlay on device hover
- **Fault Injection** — buttons to inject failures into any device for testing
- **Lockdown Device** — isolate a device from the network with one click

###  ️ Dashboard UI (Terminal 3)
- **Same 3D Room Scene** — identical geometric base, different overlay layers
- **Analytic Overlays** — ECharts panels overlaid on the 3D view (CPU, power, trends)
- **Alert Feed** — real-time WebSocket-pushed alerts with severity coloring
- **Copilot Q&A Panel** — ask natural-language questions, LLM answers with context
- **Lockdown Device** — active control (not viewer-only): isolate any device
- **Send Help** — trigger automated runbook for a failing device

### ⚙️ Backend (Terminal 2)
- **REST API** — CRUD for devices, commands, configuration (Devices UI consumes)
- **WebSocket Server** — real-time telemetry push to Dashboard UI
- **LLM Orchestrator** — fault analysis, runbook generation, anomaly detection
- **Dual Data Paths** — REST for command/response, WebSocket for push/stream

---

##  Sessions / Roadmap

| Session | Status | Deliverable |
|---------|--------|-------------|
| S1–S8 | ✅ Done | Hardware setup, Ollama, project scaffold, infra config, font install, planning docs |
| **S9A** | ⏳ Next | **Devices UI** — 3D NOC room, interactive devices, fault injection, hover panels, lockdown |
| **S9B** | ⤵️ Follows | **Dashboard UI** — 3D analytics overlays, alert feed, copilot panel, lockdown/send-help |
| S10 | 🔲 Review | Integration testing, WebSocket stress test, end-to-end verification, bug fixes |

---

## 📁 Project Structure (Final)

```
ISRO2026/
├── devices-ui/              # 📡 Terminal 1 — 3D Devices Control UI (port 5173)
│   ├── src/
│   │   ├── components/      # R3F 3D components (Room, DeviceNode, Camera, UI overlays)
│   │   ├── hooks/           # useWebSocket, useDeviceStore, useAnimation
│   │   ├── scenes/          # Canvas scene definitions
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── dashboard/               # 📊 Terminal 3 — 3D Dashboard Analytics UI (port 5174)
│   ├── src/
│   │   ├── components/      # R3F 3D components (shared patterns, different overlays)
│   │   ├── hooks/           # useWebSocket, useAlertStore, useCopilot
│   │   ├── scenes/          # Canvas scene definitions
│   │   ├── panels/          # ECharts + analytics overlay components
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── backend/                 # 🖥️ Terminal 2 — FastAPI server (port 8000)
│   ├── app/
│   │   ├── api/             # REST endpoints
│   │   ├── ws/              # WebSocket handlers
│   │   ├── llm/             # Qwen3 integration
│   │   ├── models/          # Pydantic schemas
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── info/                    # Documentation (these files)
├── .gitignore
├── README.md
├── SR.md                    # 🔒 Secrets + rules (gitignored — not tracked)
└── final.md                 # ISRO portal submission content
```

---

##  Fonts Installed
- **Inter** — sans-serif UI text (Labels, tooltips, panels)
- **JetBrains Mono** — monospace for telemetry values, terminal output, code excerpts

Check: `fc-list | grep -i inter` / `fc-list | grep -i "jetbrains mono"`

---

##  Scripts Reference

```bash
# Start all 3 terminals (dev mode)
# Terminal 1 — Devices UI
cd devices-ui && npm run dev

# Terminal 2 — Backend (separate terminal)
cd backend && uvicorn app.main:app --reload --port 8000

# Terminal 3 — Dashboard UI (separate terminal)
cd dashboard && npm run dev

# Build for production
cd devices-ui && npm run build
cd dashboard && npm run build
cd backend && docker build -t isro-backend .
```

---

##  Data Flow Summary

```
Devices UI ──REST──▶ Backend ──WebSocket──▶ Dashboard UI
               ◀──REST──       ◀──WS ack──
```

- **Devices UI** sends commands via HTTP REST, receives immediate responses
- **Backend** processes commands, runs LLM analysis, pushes telemetry/alerts via WebSocket
- **Dashboard UI** subscribes to WebSocket stream, displays real-time data overlays + alert feed + copilot

---

## 📜 License & Context
Built for **ISRO BAS 2026 — Challenge 13**. Solo team submission under Team Cyber Assassins.
