# Frontend Architecture — PS13

Two independent React applications sharing a Zustand state pattern and custom animation layer.

---

## Terminal 1: Network Topology UI (port 5173)

3D NOC visualization of a multi-site MPLS/SD-WAN network using Three.js + R3F. Displays router meshes, link lines, BGP peer relationships, and fault injection controls.

### Tech Stack
- React 18 + Vite (fast HMR, no webpack config)
- Three.js via R3F (@react-three/fiber)
- @react-three/drei (OrbitControls, Html, Text, Line, Edges)
- Zustand (store for simulation state, selections, fault params)
- anime.js (timeline animations for link traffic, alerts, transitions)

### Component Tree
```
App
├── Canvas (R3F)
│   ├── Scene
│   │   ├── AmbientLight + DirectionalLight + PointLight
│   │   ├── OrbitControls (zoom/pan/rotate)
│   │   ├── Grid (floor reference)
│   │   │
│   │   ├── SiteGroup[4] (Bangalore, Mumbai, Chennai, Delhi)
│   │   │   ├── RouterMesh[1..3 per site] (PE/P/CE/IPsec)
│   │   │   │   ├── BoxGeometry body (color-coded by role)
│   │   │   │   ├── PortIndicator (port count + status dots)
│   │   │   │   └── HtmlLabel (hostname + IP + role)
│   │   │   │
│   │   │   ├── LinkLine[between routers]
│   │   │   │   ├── BufferGeometry line
│   │   │   │   ├── Color (green=up, yellow=degraded, red=down)
│   │   │   │   └── TrafficParticles (anime.js + shader)
│   │   │   │
│   │   │   └── BgpPeerIndicator (colored sphere near router)
│   │   │
│   │   ├── IpsecTunnel (dashed arc between Bang-Delhi GWs)
│   │   │
│   │   ├── MplsLspPath (highlighted path from PE1 to PE3)
│   │   │
│   │   └── AlertIndicator[floating] (triangle + severity color)
│   │
│   └── HtmlOverlay
│       └── RouterInfoPanel (click router → name, model, peers, status, links)
│
├── HUD (positioned over canvas)
│   ├── SiteSelector (click site to focus camera)
│   ├── StatusBar (network health: healthy/degraded/critical)
│   ├── Legends (router colors, link states, peer status)
│   └── Controls (reset view, auto-rotate toggle, grid toggle)
│
├── FaultInjectionPanel (slide-in from right)
│   ├── FaultToggle[7] (link fail, BGP flap, congestion, ...)
│   ├── InjectButton
│   └── ResetButton
│
└── ConnectionManager (Zustand actions)
    ├── REST poll: /api/simulation/state (5s interval)
    ├── WS subscription: /ws/topology
    └── Actions: injectFault, resetSimulation
```

### 3D Router Representation
- **PE Router**: BoxGeometry (1.2 × 1.0 × 0.6) — blue
- **P Router**: BoxGeometry (1.0 × 0.8 × 0.6) — gray
- **CE Router**: BoxGeometry (0.8 × 0.6 × 0.4) — green
- **IPsec GW**: BoxGeometry (1.0 × 0.8 × 0.6) — orange
- **Link Lines**: TubeGeometry with color-coded material (green/amber/red)
- **Traffic Particles**: PointsGeometry + PointsMaterial, animated along link path

### Ref Structures
Refs via Zustand store. R3F stores reference to each router mesh for highlight/click. Zustand central store holds:
- `simulationState` (site statuses, link statuses, fault flags)
- `selectedRouter` (currently clicked router for info panel)
- `faultParams` (active fault injection config)
- `topologyHistory` (last N topology snapshots)
- `wsConnectionStatus` (connected/disconnected/reconnecting)

3D Exceptions managed by R3F's useFrame loop:
- Link traffic animation (update Points position along path)
- Alert indicators (rotation + pulse scale)
- Router glow on fault
- Camera orbit limits (clamp to topology bounding box)

---

## Terminal 3: Analytics Dashboard (port 5174)

Flat 2D application with data panels, charts, and copilot interface. No 3D scene — the 3D topology view on T1 serves that purpose.

### Tech Stack
- React 18 + Vite
- anime.js (panel transitions, alert animations, data updates)
- ECharts (time-series charts, gauges, heatmaps)
- Zustand (store for predictions, alerts, copilot, airgap)

### Component Tree
```
App
├── Sidebar (collapsible)
│   ├── DashboardSelector (ML / Alerts / Copilot / Incidents / Airgap)
│   └── QuickStatus (network health, active alerts count, prediction count)
│
├── MainPanel (context-dependent)
│   │
│   ├── ML Prediction Panel
│   │   ├── TtiCountdown (ECharts gauge — "Next predicted incident in X min")
│   │   ├── FailureProbability (ECharts bar chart per device)
│   │   ├── TrendChart (ECharts time-series — utilization, errors, BGP state)
│   │   ├── ModelEnsembleMetrics (per-model confidence + accuracy)
│   │   └── AnomalyTimeline (ECharts scatter — outliers over time)
│   │
│   ├── Alert Correlation Panel
│   │   ├── AlertList (grouped by topology location)
│   │   ├── BlastRadiusOverlay (mini 2D network diagram with affected nodes)
│   │   ├── SeverityDistribution (ECharts donut chart)
│   │   └── CorrelatedIncidents (grouped by root cause)
│   │
│   ├── LLM Copilot Panel
│   │   ├── ChatInput (text input + query history)
│   │   ├── AnswerDisplay (structured Q1/Q2/Q3 cards)
│   │   │   ├── Q1_What card (failure type, severity, affected devices)
│   │   │   ├── Q2_Why card (root cause analysis with evidence chain)
│   │   │   └── Q3_How card (remediation steps, CLI commands, escalation)
│   │   ├── ContextSources (which runbook docs were retrieved)
│   │   └── ConfidenceScore (LLM confidence indicator)
│   │
│   ├── Playbook Suggestion Panel
│   │   ├── PlaybookList (ranked by match score)
│   │   ├── PlaybookDetail (expanded: steps, commands, expected outcome)
│   │   └── ExecuteButton (send playbook to T1 for action)
│   │
│   ├── Incidents Timeline
│   │   ├── TimelineChart (ECharts timeline with severity color-coding)
│   │   ├── IncidentDetail (expanded: duration, symptoms, resolution)
│   │   └── StatsBar (total/active/resolved count)
│   │
│   └── Air-Gap Compliance Panel
│       ├── OverallStatus (green/amber/red gauge)
│       ├── PerCheckDetail (DNS / HTTP / Process / DataFlow)
│       └── LastScanTimestamp
│
├── ConnectionManager (Zustand actions)
│   ├── WS subscription: /ws/ml (predictions)
│   ├── WS subscription: /ws/alerts (alert events)
│   ├── WS subscription: /ws/copilot (LLM responses)
│   ├── REST queries for historical data
│   └── Actions: queryCopilot, acknowledgeAlert, executePlaybook
│
└── NotificationLayer (anime.js toast stack)
    ├── NewAlert (slide-in from top, severity colored)
    ├── PredictionWindow (TTI approaching threshold)
    └── AirGapViolation (red flash)
```

### Zustand Stores (Shared Pattern)
```
store/networkStore     — topology state, device list, link states
store/predictionStore  — ML predictions, TTI, anomaly scores
store/alertStore       — active alerts, correlated incidents
store/copilotStore     — query history, current answer, context sources
store/airgapStore      — compliance checks, last scan
store/uiStore          — active panel, sidebar state, notification queue
```

---

## Design Principles

1. **No internet required** — all assets local, no CDN
2. **Real-time first** — WS push for live data, REST for history/commands
3. **Structured output** — LLM responses render as typed cards, not raw text
4. **Topology aware** — alerts and predictions always reference network graph
5. **Notification priority** — critical alerts animate, info alerts stack quietly
6. **No 2D/4D fallback** — 3D is primary for T1; T3 is purpose-built 2D dashboard
7. **State parity** — both frontends share Zustand pattern; backend mirrors via WS
