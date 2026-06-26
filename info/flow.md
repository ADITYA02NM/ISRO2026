# Data Flow Sequences — PS13

User interaction → frontend state change → REST API → backend process → UI update.

---

## Core Pipeline

```
[User clicks IndiaMap city]
       │
       ▼
[NocContext.selectCity(cityId)]
       │
       ├──► App.tsx: centerView = "orbit"
       ├──► CityOrbitView: fetch devices for city
       │       └── GET /api/cities/{cityId}/devices
       └──► ControlBar: selectedCityId updated

[User clicks device node in CityOrbitView]
       │
       ▼
[NocContext.selectDevice(deviceName)]
       │
       ├──► App.tsx: centerView = "device"
       ├──► DeviceInspector: fetch health metrics
       │       └── GET /api/devices/{cityId}_{deviceName}/health
       └──► ControlBar: selectedDeviceId updated

[User triggers fault from ControlBar]
       │
       ▼
[POST /api/events/trigger { cityId, deviceName, type }]
       │
       ▼
[Express creates alert in memory]
       │
       ├──► Alert added to alerts array (pinned: false)
       ├──► Returns updated alerts list
       └──► NocContext.loadAlerts() re-fetches

[User sends chat message]
       │
       ▼
[POST /api/chat { message, alerts }]
       │
       ├──► Express proxies to FastAPI /api/chat
       │       └── FastAPI queries Ollama with RAG context
       ├──► Returns { response: "...", timestamp }
       └──► ChatTab renders message with markdown formatting

[Header re-scan connectors]
       │
       ▼
[GET /api/system/status]
       │
       ├──► Probes: localhost:11434 (Ollama)
       ├──► Probes: localhost:8000 (FastAPI)
       ├──► Probes: docker info (Docker)
       └──► Returns: { ollama, rag, fastapi, network, docker }

[User clicks Reset Dashboard]
       │
       ▼
[POST /api/dashboard/reset]
       │
       ├──► Clears alerts, resets state
       └──► NocContext re-fetches: cities, alerts, analytics, system status
```

---

## Startup Sequence

```
1. Start Ollama (port 11434)
   └── ollama serve
   └── Verify: qwen3:8b model loaded

2. Start FastAPI + RAG (port 8000)
   └── uvicorn noc_copilot:app
   └── ChromaDB initialized (7,920 docs indexed)
   └── ML models loaded (xgboost, isolation_forest, autoencoder, prophet, tti_regressor)

3. Build + Start Express (port 3000)
   └── npm run build  (vite build)
   └── npx tsx server.ts
   └── SPA served on /
   └── REST API ready on /api/*

4. Open browser at http://localhost:3000
   └── Boot loading sequence plays
   └── IndiaMap renders with animejs entrance animation
   └── Header shows 5 status dots (all green)
   └── Ready for interaction
```

---

## Complete Incident Lifecycle (Example)

```
Time    Event                                               Component
────    ─────                                               ─────────
T+0s    User selects Bangalore on IndiaMap                  IndiaMap → NocContext
T+0.5s  CityOrbitView renders with 4 device nodes           CityOrbitView
T+1s    User clicks P1 device → DeviceInspector shows       DeviceInspector
T+2s    Health metrics: CPU 23%, Memory 41%, uptime 14d    GET /api/devices/blr_P1/health
T+3s    User selects fault type: "Link Congestion"          ControlBar
T+4s    User clicks Trigger                                 ControlBar
T+5s    POST /api/events/trigger → alert created            Express
T+5.5s  Alert appears in LeftPanel (pinnable, deletable)    LeftPanel
T+6s    Toast notification: "⚠️ Link Congestion - P1"       App.tsx Toast
T+8s    User asks: "what happened to Bangalore P1?"         ChatTab
T+10s   POST /api/chat → FastAPI → Ollama → RAG context    Chat flow
T+15s   Response: "Link congestion detected on P1..."      ChatTab (markdown)
T+20s   User pins the alert                                 LeftPanel (PATCH /pin)
T+25s   User triggers random burst (4 faults)               ControlBar
T+30s   All alerts visible, sorted by pin + timestamp       LeftPanel
T+35s   User resets dashboard                               POST /api/dashboard/reset
T+36s   Clean state, ready for next exercise
```

---

## REST API Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/cities | List 4 cities (BLR, DEL, BOM, MAA) |
| GET | /api/cities/:cityId/devices | Devices per city |
| GET | /api/alerts | All alerts (pinned first, newest first) |
| GET | /api/alerts/summary | Severity counts |
| GET | /api/devices/:deviceId | Single device details |
| GET | /api/devices/:deviceId/health | Health metrics |
| GET | /api/system/status | All service probes |
| GET | /api/analytics | Dashboard analytics |
| POST | /api/events/trigger | Inject fault with city/device/type |
| POST | /api/events/random-burst | 4 random faults |
| PATCH | /api/alerts/:id/pin | Toggle pin |
| DELETE | /api/alerts/:id | Delete alert |
| POST | /api/chat | LLM chat with context |
| POST | /api/dashboard/reset | Full reset |

## FastAPI Endpoints (port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/health | Health check + LLM latency + RAG count |
| POST | /api/chat | Chat with Ollama (RAG-augmented) |
| POST | /predict | ML prediction from telemetry data |
