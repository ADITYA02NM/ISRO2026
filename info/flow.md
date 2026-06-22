# 🔄 Data & Interaction Flows

## 3-Terminal Architecture Flow

```
  ┌───────────────────────────────────────────────────────────────────────────┐
  │                         3-TERMINAL ARCHITECTURE FLOW                       │
  ├───────────────────────────────────────────────────────────────────────────┤
  │                                                                           │
  │  TERMINAL 1 — Devices UI (5173)          TERMINAL 3 — Dashboard (5174)    │
  │  ┌────────────────────────┐              ┌──────────────────────────────┐ │
  │  │  R3F 3D NOC Room       │              │  R3F 3D Analytics Scene      │ │
  │  │  ┌──────┐  ┌────────┐  │              │  ┌──────────┐  ┌──────────┐  │ │
  │  │  │ Dev  │  │ Dev    │  │  click/hover  │  │ 3D Room  │  │ Animated │  │ │
  │  │  │ Node1│  │ Node2  │──┼───────────────┼──│ Overlays  │  │ Graphs   │  │ │
  │  │  └──────┘  └────────┘  │              │  └──────────┘  └──────────┘  │ │
  │  └────────┬───────────────┘              └──────┬─────────┬─────────────┘ │
  │           │  show panel                         │         │               │
  │           ▼                                     │         │               │
  │  ┌────────────────────────┐                     │         │               │
  │  │  HTML Overlay Panel    │                     ▼         ▼               │
  │  │  ┌────────────────────┐│              ┌──────────┐ ┌──────────┐        │
  │  │  │ Fault Injection    ││              │ Alert    │ │ ECharts │        │
  │  │  │ Lockdown Button    ││              │ Feed     │ │ CPU/Pwr │        │
  │  │  │ Info Display       ││              │ Copilot  │ │ Trends  │        │
  │  │  └────────┬───────────┘│              └────┬─────┘ └──────────┘        │
  │  └───────────┼────────────┘                   │                           │
  │              │  HTTP POST                     │  WebSocket data            │
  │              ▼                                ▼                           │
  │  ┌────────────────────────────────────────────────────────────────────┐   │
  │  │         TERMINAL 2 — FastAPI Backend (Port 8000)                    │   │
  │  │         ─────────────────────────────────────                       │   │
  │  │                                                                     │   │
  │  │  ┌──────────────────────┐     ┌──────────────────────────────┐     │   │
  │  │  │  REST Layer          │     │  WebSocket Layer              │     │   │
  │  │  │  ───────────         │     │  ───────────────              │     │   │
  │  │  │  GET/POST /api/      │     │  /ws/telemetry (every 5s)   │     │   │
  │  │  │  /devices/:id        │◄───►│  /ws/alerts (on event)       │     │   │
  │  │  │  /satellites/:id     │     │  /ws/copilot (LLM stream)    │     │   │
  │  │  │  /faults             │     │  /ws/status (health check)   │     │   │
  │  │  └─────────┬────────────┘     └─────────────┬────────────────┘     │   │
  │  │            │                                │                       │   │
  │  │            ▼                                ▼                       │   │
  │  │  ┌────────────────────────────────────────────────────────────┐     │   │
  │  │  │  LLM Orchestrator — Qwen3-8B + Qwen3-4B (Ollama)           │     │   │
  │  │  │  ─────────────────────────────────────────────────────       │     │   │
  │  │  │  • Fault analysis & severity  │  • Runbook generation       │     │   │
  │  │  │  • Copilot streaming Q&A      │  • Alert enrichment        │     │   │
  │  │  └───────────────────────────────┬────────────────────────────┘     │   │
  │  │                                  │                                  │   │
  │  │                                  ▼                                  │   │
  │  │  ┌────────────────────────────────────────────────────────────┐     │   │
  │  │  │         Device State / Telemetry Data Store                 │     │   │
  │  │  │  ─────────────────────────────────────────────────────       │     │   │
  │  │  │  Satellite Fleet  ·  Ground Antennas  ·  Rovers              │     │   │
  │  │  │  Sensors  ·  Power Systems  ·  Comm Links  ·  All Devices    │     │   │
  │  │  └────────────────────────────────────────────────────────────┘     │   │
  │  └────────────────────────────────────────────────────────────────────┘   │
  │                                                                           │
  │  DATA PATHS:                                                              │
  │  ───────────                                                              │
  │  REST (T1 ←→ T2):  Device commands, fault injection, lockdown, status     │
  │  WS (T2 → T3):     Telemetry push, alert events, copilot streaming        │
  │  Hybrid (T3 → T2): Lockdown via REST, Send Help via WS→LLM               │
  └───────────────────────────────────────────────────────────────────────────┘
```

## Data Flow — REST Path (Devices UI ↔ Backend)

```
REST SEQUENCE — Device Interaction (T1 → T2 → T1)

 Operator        Devices UI      Zustand Store    Fetch API (REST)   FastAPI Backend   Qwen3-8B LLM
    │                │                │                  │                  │               │
    │──click dev────▶│                │                  │                  │               │
    │                │──selectDevice─▶│                  │                  │               │
    │                │◀───highlight───│                  │                  │               │
    │                │  show panel    │                  │                  │               │
    │                │                │                  │                  │               │
    │──Inject Fault─▶│                │                  │                  │               │
    │                │──toggleFault──▶│                  │                  │               │
    │                │                │──POST /fault────▶│                  │               │
    │                │                │  {type}          │──────forward────▶│               │
    │                │                │                  │                  │──analyze─────▶│
    │                │                │                  │                  │◀─severity+rec─│
    │                │                │                  │◀──200 OK────────│               │
    │                │                │◀─update state    │  {status,faultId}│               │
    │                │◀──re-render────│                  │                  │               │
    │                │  (red pulse)   │                  │                  │               │
    │                │                │                  │                  │               │
    │──Lockdown──────▶│                │                  │                  │               │
    │                │──toggleLockdown│                  │                  │               │
    │                │──(id)─────────▶│                  │                  │               │
    │                │                │──POST /lockdown─▶│                  │               │
    │                │                │                  │─────toggle──────▶│               │
    │                │                │                  │◀──200 OK────────│               │
    │                │                │◀─update lock     │  {locked:true}   │               │
    │                │◀──show lock────│                  │                  │               │
    │                │  icon + glow   │                  │                  │               │
    │                │                │                  │                  │               │

 NOTES:
   • REST is stateless — each request opens a fresh HTTP connection
   • Zustand store is the single source of truth for UI state
   • R3F re-renders from store changes (no direct REST→R3F coupling)
   • LLM analysis is synchronous within the request lifecycle
```

## Data Flow — WebSocket Path (Backend → Dashboard UI)

```
WEBSOCKET SEQUENCE — Telemetry, Alerts & Copilot (T2 → T3)

 ──── TELEMETRY PUSH (every 5s) ────────────────────────────────────────

 FastAPI         WS Server        Dashboard UI      Zustand Store      R3F Scene       ECharts
   │                │                  │                  │               │              │
   │──push 5s snap─▶│                  │                  │               │              │
   │                │──{devId,cpu,pwr}─▶                  │               │              │
   │                │──{temp,status}───▶                  │               │              │
   │                │                  │──updateTelemetry▶│               │              │
   │                │                  │                  │──color───▶    │              │
   │                │                  │                  │  health       │              │
   │                │                  │                  │──update─────▶│              │
   │                │                  │                  │  chart data   │              │
   │                │                  │                  │               │              │

 ──── ALERT EVENT ──────────────────────────────────────────────────────

 FastAPI         WS Server        LLM             Dashboard UI      Zustand Store      R3F Scene   Alert Feed
   │                │               │                  │                  │               │            │
   │──alert fires──▶│               │                  │                  │               │            │
   │                │──classify────▶│                  │                  │               │            │
   │                │◀─CRITICAL/───│                  │                  │               │            │
   │                │  WARN/INFO   │                  │                  │               │            │
   │                │──push alert─▶│                  │                  │               │            │
   │                │  {id,devId,  │                  │                  │               │            │
   │                │   sev,msg,ts}│                  │                  │               │            │
   │                │               │                  │──addAlert──────▶│               │            │
   │                │               │                  │                  │──flash───────▶│            │
   │                │               │                  │                  │  red outline  │            │
   │                │               │                  │                  │──append──────▶│            │
   │                │               │                  │                  │  new entry    │            │

 ──── COPILOT Q&A (streaming) ──────────────────────────────────────────

 Copilot Panel     WS Client        FastAPI          LLM              Zustand Store
      │                │               │               │                   │
      │──send query───▶│               │               │                   │
      │  "Why is sat 3 │──forward────▶│               │                   │
      │   overheating?" │               │──query──────▶│                   │
      │                │               │  w/ context   │                   │
      │                │               │◀─stream token─│                   │
      │                │               │  "The"        │                   │
      │                │◀─token─"The"──│               │                   │
      │◀──display──────│               │               │                   │
      │  "The"         │               │               │                   │
      │                │               │◀─stream token─│                   │
      │                │               │  "satellite"  │                   │
      │                │◀─token─"sat"─│               │                   │
      │◀──append───────│               │               │                   │
      │                │               │  ...stream continues...           │
      │                │               │               │                   │
      │                │               │◀─DONE +───────│                   │
      │                │               │  sources[]    │                   │
      │◀──final────────│               │               │                   │
      │  response+src  │               │               │                   │

 NOTES:
   • WS connections persist for the lifetime of Dashboard UI session
   • Auto-reconnect with exponential backoff: 1s, 2s, 4s, 8s, 16s (max 30s)
   • Heartbeat ping/pong every 30s to keep connection alive
   • Copilot streaming uses Server-Sent Events pattern over WebSocket
```

## User Interaction Flow — Devices UI

```
┌─────────────────────────────────────────────┐
│           DEVICES UI INTERACTION MAP          │
├─────────────────────────────────────────────┤
│                                              │
│  ┌──────────────┐                            │
│  │ 3D NOC Room  │  Camera orbit (OrbitControls)│
│  │  Loaded      │  Devices rendered in 3D     │
│  └──────┬───────┘                            │
│         │                                     │
│         ▼                                     │
│  ┌──────────────┐   mouse hover               │
│  │ Device Node   │─────────────────────────▶  │
│  │ [Hover]      │   Show info panel           │
│  └──────┬───────┘   (Anime.js enter)          │
│         │                                     │
│         ▼                                     │
│  ┌──────────────┐                             │
│  │ Device Panel │  Displays:                  │
│  │ (Anime.js)   │  - Name, type, status       │
│  │              │  - Telemetry summary        │
│  │              │  - Fault buttons            │
│  │              │  - Lockdown button          │
│  └──────┬───────┘                             │
│         │                                     │
│         ├──────────▶ "Inject Fault"           │
│         │              POST /api/devices/:id/fault│
│         │              → Device shows red pulse │
│         │                                     │
│         └──────────▶ "Lockdown"               │
│                      POST /api/devices/:id/lockdown│
│                      → Device shows lock icon  │
│                      → Network lines disabled   │
└─────────────────────────────────────────────┘
```

## User Interaction Flow — Dashboard UI

```
┌─────────────────────────────────────────────┐
│         DASHBOARD UI INTERACTION MAP          │
├─────────────────────────────────────────────┤
│                                              │
│  ┌──────────────┐   WebSocket auto-updates   │
│  │ 3D Room      │◀─────────────────────────  │
│  │ + Overlays   │   Telemetry data flows     │
│  └──────┬───────┘   Device colors update     │
│         │                                     │
│         ▼                                     │
│  ┌──────────────────────────────┐             │
│  │ Alert Feed (auto-scroll)    │             │
│  │  • 🔴 CRITICAL: Sat 3 temp │──click──▶  │
│  │  • 🟡 WARNING: Antenna 1   │  Select     │
│  │  • 🔵 INFO: Rover diagnostic│  device     │
│  └──────────────────────────────┘             │
│         │                                     │
│         ▼                                     │
│  ┌──────────────────────────────┐             │
│  │ Copilot Q&A Panel           │             │
│  │ [Operator]: "What's wrong   │             │
│  │             with Sat 3?"    │──send──▶   │
│  │ [Copilot]: "Satellite 3 is │             │
│  │  overheating. Recommend    │◀──stream──  │
│  │  reducing power draw..."   │  LLM tokens  │
│  └──────────────────────────────┘             │
│         │                                     │
│         ├──────────▶ "Lockdown Device"        │
│         │              POST /api/devices/:id/lockdown│
│         │                                     │
│         └──────────▶ "Send Help"              │
│                        WebSocket → LLM        │
│                        Generate runbook       │
└─────────────────────────────────────────────┘
```

## Dual Data Path Summary

```
                    ┌───────────┐
                    │  Operator │
                    └─────┬─────┘
                          │
            ┌─────────────┴─────────────┐
            │                           │
            ▼                           ▼
    ┌───────────────┐         ┌──────────────────┐
    │ Devices UI    │         │ Dashboard UI     │
    │ REST Client   │         │ WebSocket Client │
    └───────┬───────┘         └────────┬─────────┘
            │                          │
            │ HTTP POST/GET            │ WebSocket (ws://)
            │                          │
            ▼                          ▼
    ┌─────────────────────────────────────────┐
    │          FastAPI Backend :8000           │
    │                                          │
    │  REST Layer          WebSocket Layer     │
    │  ┌──────────┐       ┌──────────────┐    │
    │  │ CRUD     │       │ /ws/telemetry│    │
    │  │ Commands │       │ /ws/alerts   │    │
    │  │ Config   │       │ /ws/copilot  │    │
    │  └──────────┘       │ /ws/status   │    │
    │                     └──────────────┘    │
    └─────────────────────────────────────────┘
```

## Connection Lifecycle

### REST (Devices UI)
```
Request ──▶ Backend processes ──▶ Response ──▶ Connection closed
```
Stateless. Each interaction opens a fresh HTTP connection.

### WebSocket (Dashboard UI)
```
1. Client connects:  new WebSocket('ws://localhost:8000/ws/telemetry')
2. Server accepts:   WebSocket connection established
3. Server pushes:    { telemetry data } every 5s
4. Client receives:  Store update → R3F re-render
5. On disconnect:    Auto-reconnect with exponential backoff (1s, 2s, 4s, 8s...)
6. Heartbeat:        Ping/pong every 30s to keep alive
```

## Port Allocation

| Port | Service | Protocol | Assigned To |
|------|---------|----------|-------------|
| 5173 | Devices UI | HTTP (Vite dev server) | Terminal 1 |
| 8000 | FastAPI Backend | HTTP + WebSocket | Terminal 2 |
| 5174 | Dashboard UI | HTTP (Vite dev server) | Terminal 3 |
