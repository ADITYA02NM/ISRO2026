# 🎨 Frontend Architecture — Dual 3D React Apps

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND ARCHITECTURE                         │
│                                                                  │
│  TERMINAL 1                          TERMINAL 3                 │
│  devices-ui/ :5173                   dashboard/ :5174           │
│  ┌─────────────────────┐            ┌─────────────────────┐     │
│  │ React + Vite        │            │ React + Vite        │     │
│  │ + R3F + drei        │            │ + R3F + drei        │     │
│  │ + Three.js          │            │ + Three.js          │     │
│  │ + Anime.js v4       │            │ + Anime.js v4       │     │
│  │                     │            │ + ECharts           │     │
│  │ [3D NOC Room]       │            │ [3D Room +          │     │
│  │  ├─ Ground          │            │  Analytics]         │     │
│  │  ├─ Lighting        │            │  ├─ Ground          │     │
│  │  ├─ Device Nodes    │            │  ├─ Lighting        │     │
│  │  │  ├─ Satellite🔴 │            │  ├─ Device Nodes🔵 │     │
│  │  │  ├─ Antenna 🟢  │            │  │  ├─ Satellite    │     │
│  │  │  ├─ Rover  🟡   │            │  │  ├─ Antenna      │     │
│  │  │  └─ Module 🟣  │            │  │  ├─ Rover        │     │
│  │  └─ Camera Orbit   │            │  │  └─ Module       │     │
│  │                     │            │  └─ Camera Orbit    │     │
│  │ Overlays:           │            │                     │     │
│  │  ├─ Hover Info Panel│            │ Overlays:           │     │
│  │  ├─ Fault Inject    │            │  ├─ ECharts Analytics│     │
│  │  └─ Lockdown Button │            │  ├─ Alert Feed      │     │
│  │                     │            │  ├─ Copilot Q&A     │     │
│  └─────────┬───────────┘            │  ├─ Lockdown        │     │
│            │ REST                   │  └─ Send Help       │     │
│            ▼                        └─────────┬───────────┘     │
│  ┌──────────────────┐                        │ WS push         │
│  │   FastAPI REST   │                        ▼                 │
│  │   + WebSocket    │◄───────────────────────┘                 │
│  └──────────────────┘                                          │
└─────────────────────────────────────────────────────────────────┘
```

**Both frontends are strictly 3D.** No flat/2D UI fallback. The same base room scene is rendered in both, differentiated entirely by the overlay layers.

---

## Devices UI — Component Tree (Terminal 1)

```
<App>
├── <Canvas>                                // R3F Canvas
│   ├── <ambientLight />                    // drei helpers
│   ├── <directionalLight />
│   ├── <OrbitControls />                   // drei — camera orbit
│   ├── <Ground />                          // RoundedBox / Plane
│   ├── <DeviceNode position=[x,0,z]>       // per device
│   │   ├── <Satellite />                   // geometric mesh
│   │   │   ├── box (body)
│   │   │   └── cylinder (dish)
│   │   ├── <Antenna />                     // geometric mesh
│   │   ├── <Rover />                       // geometric mesh
│   │   └── <Module />                      // geometric mesh
│   ├── <DeviceInfoBubble />                 // HTML overlay on hover (raycast)
│   └── <GridHelper />
├── <UIOverlay>                              // HTML overlay (positioned absolute)
│   ├── <HoverInfoPanel />                   // anime.js animated
│   ├── <FaultInjectionPanel />              // buttons per device type
│   ├── <LockdownButton>                     // toggle isolation
│   └── <DeviceStatusBar>                    // bottom bar, all devices summary
└── </App>
```

### State Management (Devices UI)
```
Zustand Store: useDeviceStore
├── devices: Map<id, Device>
├── selectedDevice: id | null
├── hoveredDevice: id | null
├── lockedDevices: Set<id>
├── faultyDevices: Set<id>
├── selectDevice(id)
├── hoverDevice(id | null)
├── toggleFault(id, type)
├── toggleLockdown(id)
└── updateDeviceTelemetry(id, data)    // from REST poll
```

### REST Data Flow
```
[CANVAS EVENT] ──raycast──▶ [DeviceNode click/hover]
                                 │
                                 ▼
                         [Zustand Store]
                         selectDevice(id)
                         hoverDevice(id)
                                 │
                                 ▼
                         [Fetch API]
                         POST /api/devices/:id/command
                         POST /api/devices/:id/fault
                         POST /api/devices/:id/lockdown
                                 │
                                 ▼
                         [FastAPI Backend]
                         ── process command ──▶ response
                                 │
                                 ▼
                         [Zustand Store update]
                         UI re-render (R3F + HTML overlays)
```

---

## Dashboard UI — Component Tree (Terminal 3)

```
<App>
├── <Canvas>                                // R3F Canvas
│   ├── <ambientLight />
│   ├── <directionalLight />
│   ├── <OrbitControls />
│   ├── <Ground />
│   ├── <DeviceNode position=[x,0,z]>       // per device
│   │   ├── <Satellite />
│   │   ├── <Antenna />
│   │   ├── <Rover />
│   │   └── <Module />
│   └── <GridHelper />
├── <UIOverlay>
│   ├── <AnalyticsPanel>                     // ECharts
│   │   ├── <CpuGauge />                    // echarts gauge
│   │   ├── <PowerBar />                    // echarts bar
│   │   └── <TrendLine />                   // echarts line
│   ├── <AlertFeed>                         // anime.js flash on new alert
│   │   ├── <AlertItem severity=critical />
│   │   ├── <AlertItem severity=warning />
│   │   └── <AlertItem severity=info />
│   ├── <CopilotPanel>
│   │   ├── <ChatInput />
│   │   └── <ChatMessage>                   // streaming LLM response
│   ├── <LockdownButton>                    // REST: POST /lockdown
│   └── <SendHelpButton>                    // WS: trigger runbook
└── </App>
```

### State Management (Dashboard UI)
```
Zustand Store: useDashboardStore
├── devices: Map<id, Device>              // updated via WS
├── telemetry: Map<id, TelemetryData>     // updated via WS
├── alerts: Alert[]                       // pushed via WS
├── copilotMessages: Message[]
├── selectedDevice: id | null
├── addAlert(alert)                       // from WS
├── updateTelemetry(data)                 // from WS
├── sendCopilotMessage(text)              // → WS → LLM → WS stream
├── lockdownDevice(id)                    // REST
└── sendHelp(id)                          // WS → LLM runbook
```

### WebSocket Data Flow
```
[Backend WebSocket Server]
         │
         ├── /ws/telemetry  ──▶ push every 5s:
         │       { deviceId, cpu, power, temp, status, timestamp }
         │
         ├── /ws/alerts     ──▶ push on event:
         │       { id, deviceId, severity, message, timestamp }
         │
         ├── /ws/copilot    ──▶ bidirectional:
         │       ← user sends: { text: "why is satellite 3 overheating?" }
         │       → server streams: { token: "The" }
         │       → server streams: { token: "satellite" }
         │       → ... (LLM stream via Ollama)
         │
         └── /ws/status     ──▶ push every 15s:
                 { uptime, connectedDevices, wsClients, llmStatus }
         │
         ▼
[Zustand Store update] ──▶ React re-render
```

---

## Animation Strategy (Both UIs)

| Context | Engine | Examples |
|---------|--------|----------|
| 3D object animation | Three.js / R3F springs | Device rotation, orbit paths, pulse rings |
| 3D scene transitions | drei transitions | Camera fly-to, device spotlight |
| UI overlay enter/exit | Anime.js v4.4.1 | Panel slide-in, alert flash, tooltip fade |
| UI continuous motion | Anime.js v4.4.1 | Loading shimmer, pulsing status indicators |
| Scroll-based (if needed) | Anime.js scroll() | Timeline scrubbing, historical data scrub |

**Anime.js v4.4.1 Syntax:**
```js
import { animate, stagger, scroll } from 'animejs'

// Enter animation
animate('.panel', {
  translateY: [50, 0],
  opacity: [0, 1],
  duration: 400,
  easing: 'easeOutCubic'
})

// Stagger children
animate('.alert-item', {
  opacity: [0, 1],
  translateX: [-20, 0],
  delay: stagger(80)
})
```

---

## Shared 3D Components (Both UIs)

Both frontends will share the same R3F component patterns (adapted for each context):

```jsx
// Ground plane
const Ground = () => (
  <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.5, 0]}>
    <planeGeometry args={[20, 20]} />
    <meshStandardMaterial color="#1a1a2e" />
  </mesh>
)

// Orbital camera
import { OrbitControls } from '@react-three/drei'
const CameraController = () => (
  <OrbitControls
    minDistance={5}
    maxDistance={25}
    maxPolarAngle={Math.PI / 2.5}
    enableDamping
  />
)
```

---

## Why Two Apps Instead of One?

| Factor | Single App | Two Apps |
|--------|-----------|----------|
| Bundle size | Large (ECharts + analytics + controls all in one) | Smaller, focused bundles |
| Dev velocity | Must build both simultaneously | Can do S9A (Devices UI) then S9B (Dashboard UI) |
| Focus | Operators see both control + analytics | Separation of concerns |
| Port complexity | Need tabs/routes/role switching | Each app is its own focused tool |
| Reuse | Shared components save code | Shared patterns (same stack) saves learning |

Both apps share identical 3D rendering foundation. The differentiation is entirely in the **overlay layer** and **data flow patterns** (REST vs WebSocket).
