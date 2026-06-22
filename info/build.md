# 🔨 Build Guide — Session 9A + 9B

## Build Order

```
Session 9A ──▶ Devices UI (Terminal 1)
                 │
Session 9B ──▶ Dashboard UI (Terminal 3)
                 │
Session 10 ──▶ Integration + Review
```

---

## S9A — Devices UI Build (Terminal 1)

**Goal**: Working 3D NOC room with interactive devices, fault injection, and lockdown.

**Location**: `ISRO2026/devices-ui/`

### Step-by-Step

| Step | Task | Details |
|------|------|---------|
| 1 | Scaffold React+Vite project | `npm create vite@latest devices-ui -- --template react` |
| 2 | Install 3D dependencies | `npm install three @react-three/fiber @react-three/drei` |
| 3 | Install anime.js v4 | `npm install animejs@4.4.1` |
| 4 | Install Zustand | `npm install zustand` |
| 5 | Create basic 3D scene | `<Canvas>` with ambient/directional light, ground plane, OrbitControls |
| 6 | Add DeviceNode components | Geometric meshes: Satellite, Antenna, Rover, Module |
| 7 | Position devices in 3D space | Grid layout on ground plane |
| 8 | Add raycasting hover | R3F `onPointerOver`/`onPointerOut` → Zustand hover state |
| 9 | Build HoverInfoPanel | HTML overlay, anime.js animated enter/exit |
| 10 | Build FaultInjectionPanel | Buttons per device, POST to backend |
| 11 | Build LockdownButton | Toggle with visual confirmation |
| 12 | Connect REST endpoints | Fetch API to backend (mock or real) |
| 13 | Connect to FastAPI | (if backend is ready) or use mock |

### Devices UI Mock Strategy

When backend isn't ready yet, mock data locally:

```js
// src/mocks/devices.js
export const MOCK_DEVICES = [
  { id: 'sat-1', name: 'Satellite 1', type: 'satellite', status: 'healthy', cpu: 45, power: 120 },
  { id: 'ant-1', name: 'Antenna 1', type: 'antenna', status: 'healthy', cpu: 23, power: 80 },
  { id: 'rov-1', name: 'Rover 1', type: 'rover', status: 'warning', cpu: 78, power: 200 },
  { id: 'mod-1', name: 'Module 1', type: 'module', status: 'healthy', cpu: 34, power: 55 },
]
```

Mock API responses using Zustand initial state + timers:

```js
// src/stores/useDeviceStore.js
import { create } from 'zustand'
import { MOCK_DEVICES } from '../mocks/devices'

export const useDeviceStore = create((set, get) => ({
  devices: new Map(MOCK_DEVICES.map(d => [d.id, d])),
  hoveredDevice: null,
  lockedDevices: new Set(),
  faultyDevices: new Set(),
  
  toggleFault: (id, type) => set(state => {
    const faulty = new Set(state.faultyDevices)
    if (faulty.has(id)) faulty.delete(id)
    else faulty.add(id)
    return { faultyDevices: faulty }
  }),
  
  toggleLockdown: async (id) => {
    // Mock: just toggle locally
    set(state => {
      const locked = new Set(state.lockedDevices)
      if (locked.has(id)) locked.delete(id)
      else locked.add(id)
      return { lockedDevices: locked }
    })
  }
}))
```

---

## S9B — Dashboard UI Build (Terminal 3)

**Goal**: Working 3D analytics dashboard with WebSocket alerts, copilot, and action controls.

**Location**: `ISRO2026/dashboard/` (existing directory, refactored for 3D)

### Step-by-Step

| Step | Task | Details |
|------|------|---------|
| 1 | Scaffold new React+Vite project or refactor existing | `dashboard/` — replace flat UI with R3F Canvas |
| 2 | Install 3D deps + anime.js + ECharts | `npm install three @react-three/fiber @react-three/drei animejs@4.4.1 echarts echarts-for-react zustand` |
| 3 | Create same base 3D scene | Replicate ground, lighting, device positions from Devices UI |
| 4 | Add ECharts analytics panels | CPU Gauge, Power Bar, Trend Line as HTML overlays |
| 5 | Add WebSocket client | Auto-reconnect, heartbeat, parse incoming messages |
| 6 | Connect telemetry WS → R3F scene | Device colors update from telemetry data |
| 7 | Build AlertFeed component | Severity-graded, auto-scroll, anime.js flash animation |
| 8 | Build CopilotPanel | Chat UI + WebSocket stream display |
| 9 | Add Lockdown/Send Help controls | REST POST for lockdown, WS→LLM for send-help |
| 10 | Connect to real backend | (if backend is ready) or use mock WS server |

### Dashboard UI Mock Strategy

Mock WebSocket with a local interval-based emulator:

```js
// src/mocks/wsMock.js
const MOCK_TYPES = ['satellite', 'antenna', 'rover', 'module']
const MOCK_STATUSES = ['healthy', 'healthy', 'healthy', 'warning', 'critical']  // weighted

export function startMockWebSocket(onMessage) {
  const interval = setInterval(() => {
    const deviceId = `dev-${Math.floor(Math.random() * 4) + 1}`
    const data = {
      type: 'telemetry',
      deviceId,
      cpu: Math.floor(Math.random() * 100),
      power: Math.floor(Math.random() * 250),
      temp: Math.floor(Math.random() * 50) + 20,
      status: MOCK_STATUSES[Math.floor(Math.random() * MOCK_STATUSES.length)],
      timestamp: Date.now()
    }
    onMessage(data)
    
    // Random alerts (10% chance per tick)
    if (Math.random() < 0.1) {
      onMessage({
        type: 'alert',
        deviceId,
        severity: Math.random() < 0.3 ? 'CRITICAL' : 'WARNING',
        message: `${deviceId} reporting abnormal telemetry`,
        timestamp: Date.now()
      })
    }
  }, 5000)
  
  return () => clearInterval(interval)
}
```

Mock copilot locally:

```js
// Respond to copilot questions with canned answers
const MOCK_COPILOT = {
  'overheat': 'The device is experiencing thermal stress. Recommended actions:\n1. Reduce power draw\n2. Enable secondary cooling\n3. Monitor for 5 minutes\n4. If persists, initiate lockdown',
  'default': 'I am analyzing the telemetry data. The device appears to be operating within normal parameters.'
}
```

---

## Backend Build (Reference)

Backend can be built in parallel with either frontend. It's FastAPI with:

```
backend/
├── app/
│   ├── main.py          # FastAPI app + WebSocket routes
│   ├── api/
│   │   ├── devices.py   # REST endpoints for devices
│   │   └── commands.py  # REST for commands/fault/lockdown
│   ├── ws/
│   │   ├── telemetry.py # WebSocket telemetry push
│   │   ├── alerts.py    # WebSocket alert push
│   │   └── copilot.py   # WebSocket LLM streaming
│   ├── llm/
│   │   ├── client.py    # Ollama HTTP client
│   │   └── prompts.py   # System prompts for each task
│   └── models/
│       └── schemas.py   # Pydantic models
├── requirements.txt
└── Dockerfile
```

---

## Dependency Installs (Both Frontends)

### Devices UI (`devices-ui/`)
```bash
npm install three@latest
npm install @react-three/fiber@latest
npm install @react-three/drei@latest
npm install animejs@4.4.1
npm install zustand@latest
```

### Dashboard UI (`dashboard/`)
```bash
npm install three@latest
npm install @react-three/fiber@latest
npm install @react-three/drei@latest
npm install animejs@4.4.1
npm install zustand@latest
npm install echarts@latest
npm install echarts-for-react@latest
```

---

## Testing Strategies

### Devices UI Testing
- **Visual**: Manually verify 3D room renders, OrbitControls work, device meshes appear
- **Interaction**: Click devices → info panel shows, fault injection → device state changes, lockdown → visual lock
- **REST mock**: Test with mock data first, then real backend

### Dashboard UI Testing
- **WebSocket mock**: Verify telemetry updates 3D scene, alerts populate feed
- **Copilot mock**: Verify chat UI, streaming display, markdown rendering
- **ECharts**: Verify charts update from telemetry data
- **Lockdown/Send Help**: Verify buttons dispatch correct requests

### Integration Testing (S10)
- Both frontends connect to real backend simultaneously
- Inject fault from Devices UI → verify alert appears in Dashboard UI
- Lockdown from Dashboard UI → verify device shows locked in Devices UI
- Send Help → verify LLM generates runbook in Copilot panel
- Start/stop WebSocket → verify auto-reconnect works

---

## Development Workflow

```
# Terminal 1 — Devices UI
cd devices-ui && npm run dev
# Opens at http://localhost:5173

# Terminal 2 — Backend (real or mock)
cd backend && uvicorn app.main:app --reload --port 8000
# Or use mock data in the frontend store

# Terminal 3 — Dashboard UI (separate terminal session)
cd dashboard && npm run dev
# Opens at http://localhost:5174
```

Each developer terminal can run independently. Mock data lets either frontend work without the backend being finished.
