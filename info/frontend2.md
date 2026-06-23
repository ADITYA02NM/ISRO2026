# Frontend 2 — T2 Alert & Solution Dashboard (port 8000)

Real-time alert response dashboard showing T3's analysis (Ollama LLM + rule engine). Flat 2D application with ECharts visualizations and anime.js transitions.

---

## Tech Stack

- **React 18 + Vite**
- **anime.js** (alert card animations, panel transitions, counter roll-ups)
- **ECharts** (alert timeline, severity distribution charts)
- **Zustand** (store for alerts, solutions, command state, UI)

## Component Tree

```
App
├── TopBar (persistent)
│   ├── Title ("PS13 ALERT RESPONSE • TERMINAL 2")
│   ├── T3ConnectionStatus (green/amber/red indicator)
│   │
│   └── AlertSummaryBar
│       ├── ActiveAlertsCount (critical/warning/info breakdown)
│       ├── DevicesAffectedCount
│       ├── AvgResolutionTime
│       └── LastAlertTimestamp
│
├── MainPanel (split layout)
│   │
│   ├── LeftPanel (60%) — AlertFeed
│   │   ├── FeedControls
│   │   │   ├── SeverityFilter (CRITICAL / WARNING / INFO / ALL)
│   │   │   ├── DeviceFilter (dropdown by city)
│   │   │   ├── SortToggle (time / severity)
│   │   │   ├── SearchInput
│   │   │   └── PauseResumeButton
│   │   │
│   │   └── AlertCardList (scrollable, streaming)
│   │       └── AlertCard[n] (each alert, newest at top)
│   │           ├── SeverityBadge (🔴 / 🟡 / 🟢 with severity label)
│   │           ├── Timestamp
│   │           ├── DeviceName (linked to city)
│   │           ├── AlertMessage
│   │           ├── ExpandableDetail
│   │           │   ├── TelemetrySnapshot
│   │           │   ├── AffectedRoutes
│   │           │   └── Timeline
│   │           └── ActionRow
│   │               ├── ViewSolutionButton
│   │               ├── AcknowledgeButton
│   │               └── EscalateButton
│   │
│   └── RightPanel (40%) — SolutionView
│       ├── SolutionHeader
│       │   ├── RelatedAlert summary
│       │   ├── AnalysisSource ("Ollama Qwen3-8B + Rule Engine")
│       │   └── ConfidenceBar (0-100%)
│       │
│       ├── RootCauseAnalysis
│       │   └── Structured text from LLM (cause + evidence)
│       │
│       ├── RecommendedActions
│       │   └── Numbered steps from LLM
│       │
│       ├── QuickActionButtons (ProcessingCard style)
│       │   ├── LockdownRoute → POST /api/device/:id/lockdown
│       │   ├── ResetBGP → POST /api/device/:id/bgp-reset
│       │   ├── DiagnosticMode → POST /api/device/:id/diagnostic
│       │   └── UnlockRoute → POST /api/device/:id/unlock
│       │
│       └── ExecutionStatusTracker
│           ├── Sent timestamp
│           ├── Acknowledged timestamp
│           └── Completed timestamp
│
├── BottomPanel — AlertTimeline (ECharts)
│   ├── StackedAreaChart (red=critical, amber=warning, green=info)
│   ├── TimeWindowSelector (1h / 6h / 24h / 7d)
│   ├── Click-to-filter (click point → filter alerts to that window)
│   └── IncidentMarkers (vertical lines for major events)
│
├── ControlPanel (left side, collapsible)
│   ├── AutoAcknowledgeInfoToggle
│   ├── SoundOnAlertToggle (browser notification API)
│   ├── AlertRetentionDropdown (100 / 500 / 1000)
│   ├── ThemeToggle (Response / Standard)
│   └── RefreshRateDropdown (realtime / 5s / 30s)
│
├── ConnectionManager (Zustand actions)
│   ├── WS: ws://localhost:5174/ws/alerts (live alerts)
│   ├── WS: ws://localhost:5174/ws/solutions (live solutions)
│   ├── REST: GET /api/alerts (history)
│   └── REST: POST /api/device/:id/:action (commands)
│
└── NotificationLayer (anime.js toast stack)
    ├── NewCriticalAlert (red slide-in from top)
    ├── NewWarningAlert (amber slide-in)
    ├── NewInfoAlert (green, auto-dismiss 30s)
    ├── CommandSent (brief confirmation)
    ├── StormModeActivated (red flash when >10 alerts in 60s)
    └── T3Disconnected (red flash + reconnecting spinner)
```

## Component Mapping (Reference Components)

| Component | Usage |
|-----------|-------|
| `ThemeToggleButtons` | All toggle switches in control panel |
| `ContainerScrollAnimation` | Alert feed scroll-reveal and solution panel entries |
| `SystemMonitor` | Mini-widget showing T3 health status |
| `ProcessingCard` | Solution recommendation cards and quick action buttons |
| `WorldMap` | Optional mini-map showing affected device locations |

## Zustand Stores

```
store/alertStore       — active alerts, filters, pause state, alert history
store/solutionStore    — current solution, root cause, actions, confidence
store/deviceStore      — device list, status (from T3 topology WS)
store/uiStore          — active panel, theme, auto-acknowledge, sound toggle
store/wsStore          — connection status, reconnect state
```

## Data Flow

```
T3 (port 5174)                            T2 (port 8000)
    │                                          │
    ├── WS /ws/alerts ────────────────────────►│  Live alert events
    │   { severity, device, type, message }    │
    │                                          │
    ├── WS /ws/solutions ─────────────────────►│  LLM-generated solutions
    │   { alertId, rootCause, actions }        │
    │                                          │
    │◄── POST /api/device/:id/:action ────────┤  Resolution commands
    │   { action: "lockdown" }                 │
    │                                          │
    │◄── POST /api/alerts/:id/acknowledge ────┤  Alert acknowledgement
    │                                          │
    │──► Response ────────────────────────────►│  Command result / ack status
```

## Design Principles

1. **No internet required** — all assets local, no CDN
2. **Real-time first** — WS push for live alert and solution data
3. **SOC triage aesthetic** — urgency through severity color-coding, controlled chaos
4. **Structured analysis** — LLM responses render as typed cards, not raw text
5. **Alert lifecycle** — every alert goes through: new → acknowledged → resolved
6. **State parity** — Zustand pattern shared with T1; backend mirrors via WS
