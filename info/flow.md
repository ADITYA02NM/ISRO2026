# 🔄 Data & Interaction Flows

## 3-Terminal Architecture Flow

```mermaid
flowchart TB
    subgraph T1["Terminal 1 — Devices UI (5173)"]
        direction TB
        T1_R3F["R3F 3D Scene<br/>Interactive Devices<br/>Hover Info Panels"]
        T1_UI["HTML Overlays<br/>Fault Injection<br/>Lockdown Button"]
        T1_REST["REST Client<br/>(Fetch API)"]
    end

    subgraph T2["Terminal 2 — Backend (8000)"]
        direction TB
        T2_REST["FastAPI REST Layer"]
        T2_WS["FastAPI WebSocket Layer"]
        T2_LLM["LLM Orchestrator<br/>Qwen3-8B + 4B"]
        T2_DATA["Device State<br/>Telemetry Data"]
    end

    subgraph T3["Terminal 3 — Dashboard UI (5174)"]
        direction TB
        T3_R3F["R3F 3D Scene<br/>Analytics Overlays"]
        T3_WS["WebSocket Client<br/>Auto-Reconnect"]
        T3_UI["Alert Feed<br/>Copilot Panel<br/>Lockdown + Send Help"]
        T3_ECHARTS["ECharts<br/>CPU / Power / Trends"]
    end

    T1_R3F -->|"click/hover<br/>events"| T1_UI
    T1_UI -->|"HTTP POST"| T1_REST
    T1_REST -->|"api/devices/:id/command<br/>api/devices/:id/fault<br/>api/devices/:id/lockdown"| T2_REST
    T2_REST -->|"process & respond"| T2_DATA
    T2_DATA -->|"JSON response"| T1_REST
    T1_REST -->|"state update"| T1_R3F

    T2_DATA -->|"telemetry push<br/>every 5s"| T2_WS
    T2_LLM -->|"fault analysis<br/>runbook gen"| T2_DATA
    T2_WS -->|"ws://localhost:8000/ws/telemetry"| T3_WS
    T2_WS -->|"ws://localhost:8000/ws/alerts"| T3_UI
    T2_WS -->|"ws://localhost:8000/ws/copilot"| T3_UI
    T3_WS -->|"state update"| T3_R3F
    T3_WS -->|"chart data"| T3_ECHARTS
    T3_UI -->|"lockdown request<br/>(HTTP REST)"| T2_REST
    T3_UI -->|"send help<br/>(runs LLM runbook)"| T2_LLM
```

## Data Flow — REST Path (Devices UI ↔ Backend)

```mermaid
sequenceDiagram
    participant User as 👤 Operator
    participant UI as 🖥️ Devices UI (R3F)
    participant Store as 📦 Zustand Store
    participant API as 🌐 Fetch API (REST)
    participant Backend as ⚙️ FastAPI Backend
    participant LLM as 🧠 Qwen3-8B (Ollama)

    User->>UI: Clicks device in 3D room
    UI->>Store: selectDevice(id)
    Store->>UI: Highlight device, show info panel
    User->>UI: Clicks "Inject Fault"
    UI->>Store: toggleFault(id, type)
    Store->>API: POST /api/devices/:id/fault { type }
    API->>Backend: Forward request
    Backend->>LLM: Analyze fault context
    LLM-->>Backend: Severity + recommendations
    Backend-->>API: 200 OK { status, faultId }
    API-->>Store: Update device state
    Store-->>UI: Re-render (device shows fault state)

    User->>UI: Clicks "Lockdown"
    UI->>Store: toggleLockdown(id)
    Store->>API: POST /api/devices/:id/lockdown
    API->>Backend: Toggle isolation
    Backend-->>API: 200 OK { locked: true }
    API-->>Store: Update lockdown state
    Store-->>UI: Device shows locked indicator
```

## Data Flow — WebSocket Path (Backend → Dashboard UI)

```mermaid
sequenceDiagram
    participant Backend as ⚙️ FastAPI Backend
    participant WS as 🌐 WebSocket Server
    participant LLM as 🧠 Qwen3-8B (Ollama)
    participant Client as 📡 Dashboard UI (WS Client)
    participant Store as 📦 Zustand Store
    participant Scene as 🏗️ R3F Scene
    participant Charts as 📊 ECharts Panels
    participant Alerts as ⚠️ Alert Feed

    Note over Backend,WS: Connection established
    Backend->>WS: Every 5s: push telemetry snapshot
    WS-->>Client: { deviceId, cpu, power, temp, status }
    Client->>Store: updateTelemetry(data)
    Store->>Scene: Update 3D device colors (health → color)
    Store->>Charts: Update gauge/bar/line data

    Note over Backend,Alerts: Alert event fires
    Backend->>LLM: Classify alert severity
    LLM-->>Backend: CRITICAL / WARNING / INFO
    Backend->>WS: Push alert
    WS-->>Client: { id, deviceId, severity, message, timestamp }
    Client->>Store: addAlert(alert)
    Store->>Alerts: Flash + append new alert
    Store->>Scene: Flash device outline red/amber

    Note over Backend,Client: Copilot interaction
    Client->>WS: { text: "Why is satellite 3 overheating?" }
    WS->>Backend: Forward question
    Backend->>LLM: Query with device context
    LLM-->>Backend: Stream tokens
    loop For each token
        Backend->>WS: { token: "The" }
        WS-->>Client: stream token
        Client->>Store: appendCopilotToken(token)
        Store->>Client: Update copilot display
    end
    Backend->>WS: { token: DONE, sources: [...] }
    WS-->>Client: Final response with sources
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
