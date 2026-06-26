# Frontend Architecture — PS13

Single-page React application served by Express, with a 3-panel dashboard layout, state-machine center views, and real-time alert/chat interaction.

---

## Tech Stack

- **React 18 + Vite** (fast HMR, TypeScript)
- **Tailwind CSS** (utility-first styling)
- **Three.js** via `@react-three/fiber` + `drei` (Starfield background, CityOrbitView 3D orbital rings)
- **anime.js v4** (IndiaMap entrance animations: connection line draw, node bounce, label slide)
- **Framer Motion** (`motion` + `AnimatePresence` for view transitions, toast animations)
- **Lucide React** (icons: Pin, Trash2, ScanSearch, RefreshCw, etc.)

---

## Component Tree

```
App.tsx
├── BootLoading (typewriter boot sequence, 5-step [OK] markers)
├── ToastContainer (AnimatePresence, auto-dismiss 4s)
├── Starfield (CSS animated star field background)
├── Header (logo, PS13 title, 5 service status dots, re-scan button)
├── main grid (3 columns)
│   ├── LeftPanel (320px)
│   │   ├── Network Overview (4 cities, device counts, health status)
│   │   ├── Live Alerts (pinned alerts always visible + scrollable feed)
│   │   └── ML Model Ensemble (5 models with status indicators)
│   │
│   ├── Center Panel (1fr — state-machine switches)
│   │   ├── IndiaMap (SVG outline, clickable city markers, animejs entrance)
│   │   ├── CityOrbitView (3D R3F orbital ring scene with device nodes)
│   │   └── DeviceInspector (health metrics, CPU/memory bars with shimmer)
│   │
│   └── ChatTab (340px — right panel)
│       ├── Message list (markdown formatting, timestamps)
│       ├── Typing indicator (animated dots)
│       └── Input (auto-focus on mount)
│
└── ControlBar (bottom, hidden until hover)
    ├── City selector (from context)
    ├── Device selector (from context)
    ├── Fault type selector (7 types)
    ├── Trigger button
    ├── Random Burst button
    ├── ML Predict button
    └── Reset Dashboard button
```

---

## State Management

Uses React Context API (`NocContext`):

```typescript
interface NocContextType {
  // Data
  cities: City[];
  alerts: Alert[];
  analytics: Analytics | null;
  systemStatus: SystemStatus | null;
  chatMessages: ChatMessage[];
  selectedCityId: string | null;
  selectedDeviceId: string | null;

  // Actions
  selectCity: (id: string) => void;
  selectDevice: (id: string | null) => void;
  triggerEvent: (options?: TriggerOptions) => Promise<void>;
  triggerWithML: (options?: TriggerOptions) => Promise<void>;
  sendChat: (message: string) => Promise<void>;
  pinAlert: (id: string) => Promise<void>;
  deleteAlert: (id: string) => Promise<void>;
  resetDashboard: () => Promise<void>;
  refreshData: () => Promise<void>;
}
```

---

## Center View State Machine

```
┌──────────┐    click city     ┌──────────────┐    click device    ┌──────────────────┐
│ IndiaMap │ ────────────────► │ CityOrbitView │ ────────────────► │ DeviceInspector   │
│ (default) │   selectCity()   │  (centerView  │   selectDevice()  │ (centerView       │
│           │                  │   = "orbit")  │                   │  = "device")      │
└──────────┘                  └──────────────┘                   └──────────────────┘
      ▲                                 │                                 │
      │        ESC / Back               │     "Back to Map"               │
      └─────────────────────────────────┴─────────────────────────────────┘
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Single page (no routing) | Simpler state management; no HashRouter needed |
| React Context (not Zustand) | Simpler for moderate state; no extra dependency |
| State-machine center view | Clean transitions between map→orbit→device |
| R3F for orbit views | Reuses Three.js; consistent with Starfield |
| Anime.js for entrance | One-time animations on mount; lightweight |
| Framer Motion for transitions | AnimatePresence handles exit animations cleanly |
| Tailwind | Zero runtime CSS; consistent design system |
| Pinned alerts always visible | Critical info never scrolls away |
