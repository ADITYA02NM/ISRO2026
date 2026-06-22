# 🏗️ System Architecture — Deep Dive

## 3-Terminal Topology

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       3-TERMINAL SYSTEM TOPOLOGY                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TERMINAL 1                  TERMINAL 2                  TERMINAL 3    │
│  Devices UI                  Backend                     Dashboard UI  │
│  ┌─────────────────┐       ┌────────────────────┐      ┌─────────────┐ │
│  │ React + Vite    │       │ FastAPI + Uvicorn  │      │ React+Vite  │ │
│  │ R3F + drei      │       │                    │      │ R3F + drei  │ │
│  │ Three.js        │       │ Qwen3-8B (Ollama)  │      │ Three.js    │ │
│  │ Anime.js v4     │       │ Qwen3-4B (fallback)│      │ Anime.js v4 │ │
│  │ Port 5173       │       │ Port 8000          │      │ ECharts     │ │
│  └────────┬────────┘       └──────────┬─────────┘      │ Port 5174   │ │
│           │                           │                └──────┬──────┘ │
│           │     ┌─────────────────┐   │                       │       │
│           │     │ floci.io infra  │   │                       │       │
│           │     │ (local AWS emu) │   │                       │       │
│           │     └─────────────────┘   │                       │       │
│           │                           │                       │       │
│           └──────────REST─────────────┴───────WebSocket───────┘       │
│                      ▲                             ▲                  │
│                      │                             │                  │
│              HTTP POST/GET                  WS push telemetry         │
│              commands/queries               alerts, status            │
│              immediate response             LLM stream (copilot)      │
│                                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Terminal 1 — Devices UI (port 5173)

**Role**: Interactive 3D ground control for device monitoring and fault management.

- **Framework**: React 18+ with Vite (fast HMR, optimized builds)
- **3D Engine**: React Three Fiber (`@react-three/fiber`) + drei (`@react-three/drei`) + Three.js
- **Animation Overlay**: Anime.js v4.4.1 for non-3D UI transitions (hover panels, alert highlights)
- **State Management**: Zustand (lightweight, works well with R3F)
- **HTTP Client**: Fetch API (lightweight, no axios needed for simple REST)

### Key Components
- **3D NOC Room** — full R3F scene with ground plane, ambient lighting, device nodes
- **Device Nodes** — geometric meshes (BoxGeometry/SphereGeometry) positioned in 3D space
- **Hover Info Panel** — anime.js-animated HTML overlay triggered by raycasting hover
- **Fault Injection Panel** — buttons per device type to simulate failures
- **Lockdown Controls** — single-click device isolation with visual lock state

### Data Flow (REST only)
```
User Interaction → R3F Canvas Event → Zustand Store → Fetch API → Backend REST
                                                                       ↓
UI Update ← Zustand ← Fetch Response ← Backend processes command
```

---

## Terminal 2 — Backend (port 8000)

**Role**: Central data processing, command handling, and intelligence layer.

- **Framework**: FastAPI with Uvicorn (async-first, WebSocket built-in)
- **LLM**: Ollama-hosted Qwen3-8B (primary) + Qwen3-4B-Thinking (fallback)
- **Infrastructure**: floci.io (local AWS emulation — S3-compatible storage, SQS, Lambda simulation)
- **Data**: In-memory device state + optional SQLite for persistence

### Dual Interface
| Interface | Protocol | Purpose | Consumed By |
|-----------|----------|---------|-------------|
| REST API | HTTP | CRUD for devices, run commands, query status, config | Devices UI |
| WebSocket | WS | Push telemetry, alerts, LLM copilot stream | Dashboard UI |

### LLM Integration
- **Fault Analysis**: Qwen3-8B receives device telemetry + fault context, returns root cause + severity
- **Runbook Generation**: Qwen3-4B-Thinking generates step-by-step runbook for "send help" triggers
- **Anomaly Detection**: Qwen3-8B identifies anomalous patterns in telemetry streams
- **Copilot Q&A**: Qwen3-8B answers natural-language queries about device state and history

### API Endpoints (Planned)
```
REST:
  GET    /api/devices              → list all devices
  GET    /api/devices/:id          → device detail + telemetry
  POST   /api/devices/:id/command  → execute command (recover, lockdown, etc.)
  POST   /api/devices/:id/fault    → inject fault
  POST   /api/devices/:id/lockdown → toggle isolation
  GET    /api/devices/:id/history  → telemetry history

WebSocket:
  /ws/telemetry                   → push device telemetry (5s interval)
  /ws/alerts                      → push severity-graded alerts
  /ws/copilot                     → LLM streaming Q&A
  /ws/status                      → system health + connection status
```

---

## Terminal 3 — Dashboard UI (port 5174)

**Role**: Real-time 3D monitoring, analytics, alert triage, and action dispatch.

- **Framework**: React 18+ with Vite
- **3D Engine**: React Three Fiber + drei + Three.js (same base as Devices UI)
- **Analytics**: ECharts (Apache ECharts via `echarts-for-react`) for CPU/power/trend charts
- **Animation Overlay**: Anime.js v4.4.1 for panel transitions, alert animations
- **WebSocket Client**: Native WebSocket (auto-reconnect, heartbeat)
- **State Management**: Zustand

### Key Components
- **Same 3D Room Scene** — shared geometric layout, different context overlay
- **Analytic Panels** — ECharts panels (CPU gauge, power bar, trend lines) rendered as HTML overlays
- **Alert Feed** — real-time WebSocket push, severity: CRITICAL/WARNING/INFO, with anime.js flash
- **Copilot Q&A** — text input → WebSocket GET → LLM stream → rendered markdown-style answer
- **Lockdown / Send Help** — buttons that dispatch commands via REST (lockdown isolation) or via WebSocket/LLM (send help → auto-runbook)

### Data Flow (WebSocket primary)
```
Backend → WebSocket Push → Zustand Store → R3F Scene update (telemetry)
                                        → Alert Feed (alert list)
                                        → Copilot Panel (LLM stream)
                                        → ECharts (chart data update)
```

---

## Data Layer Summary

| Aspect | REST (Terminal 1 ↔ 2) | WebSocket (Terminal 2 → 3) |
|--------|----------------------|---------------------------|
| Protocol | HTTP/1.1 | WS (RFC 6455) |
| Direction | Bidirectional request/response | Server → Client push |
| Frequency | On-demand (user actions) | Continuous (5s telemetry) |
| Payload | JSON | JSON (serialized) |
| State | Stateless | Stateful connection |
| Use Case | Commands, queries, config | Telemetry, alerts, LLM stream |

---

## Security Considerations

- **No authentication** in v1 — internal network assumption (floci.io sandbox)
- **Lockdown API** requires explicit confirmation (double-tap)
- **Send Help** triggers read-only runbook generation (no auto-execution without confirmation)
- **SR.md** contains GitHub PAT — .gitignored, never committed
- All LLM inference is local — no data leaves the machine

---

## Why 3 Terminals?

The decision to split into **two separate frontends** (not one combined app) was deliberate:

| Factor | Single Combined App | Two Separate Apps |
|--------|-------------------|-------------------|
| Complexity | One large bundle, complex routing | Two focused codebases |
| Development | Both devs block each other | Parallel development |
| Portability | Monolithic deploy | Independent deploy |
| Focus | Control + Analytics mixed | Clear separation of concerns |
| WebSocket | Shared connection | Dedicated per dashboard |
| Build Time | Longer single build | Shorter independent builds |
| Learning | One set of dependencies | Same stack x2 (reusable skills) |

Both apps share the **same 3D rendering stack** (R3F + drei + Three.js) but have **different overlay layers and interaction models**. This allows each to be optimized independently without cascading changes.
