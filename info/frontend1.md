# Frontend 1 — T1 Operator Console (port 5173)

3D mission-control console for commanding devices across a multi-site MPLS network. Uses Three.js + R3F for the India map visualization and anime.js for packet animation.

---

## Tech Stack

- **React 18 + Vite** (fast HMR, no webpack config)
- **Three.js via R3F** (`@react-three/fiber`)
- **`@react-three/drei`** (CameraControls, Html, Text, Line, Edges)
- **Zustand** (store for device state, command history, UI panels)
- **anime.js** (timeline animations for packet arcs, panel transitions, HUD effects)

## Component Tree

```
App
├── Canvas (R3F)
│   ├── Scene
│   │   ├── AmbientLight + DirectionalLight + PointLight
│   │   ├── CameraControls (zoom/pan/rotate, auto-orbit)
│   │   ├── Starfield (parallax particle system, background)
│   │   │
│   │   ├── WorldMap (GeoSJON India outline — glowing wireframe)
│   │   │
│   │   ├── CityNode[4] (Bangalore, Mumbai, Chennai, Delhi)
│   │   │   ├── GlowRing (pulsating outer ring)
│   │   │   ├── StatusDot (online/offline, WS-driven)
│   │   │   ├── SatelliteOrbits (tiny sphere orbiting via radial-orbital-timeline)
│   │   │   ├── LightCone (soft searchlight upward)
│   │   │   └── HtmlLabel (city name, Orbitron font)
│   │   │
│   │   ├── PacketArc[multiple] (anime.js timeline)
│   │   │   ├── Bezier curve between cities
│   │   │   ├── Glowing sphere (~4px) along path
│   │   │   ├── Motion trail (fade effect)
│   │   │   └── Color: cyan(command) / amber(anomaly) / green(ack)
│   │   │
│   │   ├── RippleEffect (emitted on command success at target node)
│   │   │
│   │   └── HUD (positioned over canvas, not in 3D scene)
│   │       ├── TopBar ("PS13 MISSION CONTROL • TERMINAL 1" + time + record dot)
│   │       ├── T3LinkStatus (signal bars, green/amber/red)
│   │       ├── DeviceCounter ("DEVICES: 4/4 ONLINE" from WS)
│   │       ├── CommandCounter ("COMMANDS FIRED: 12")
│   │       └── Heartbeat (pulse animation, WS ping/pong)
│   │
│   └── HtmlOverlay (DOM overlays on canvas)
│       ├── DeviceDetailPanel (click node → zoom + slide-in)
│       │   ├── DeviceInfo (name, city, status, uptime)
│       │   ├── LiveMetrics (latency, throughput, packetLoss — from WS)
│       │   └── ActionButtonGrid (Ping, Traceroute, Bounce, Anomaly, Lockdown, Diagnostic)
│       │       ├── Loading spinner per button
│       │       ├── Result display on completion (ProcessingCard style)
│       │       └── ConfirmationDialog for destructive actions
│       │
│       └── CommandHistory (collapsible panel, left side)
│           ├── Scrollable log (timestamp + action + device + status)
│           ├── Status icons: ⏳ → ✅ → ❌
│           ├── Click to re-fire any command
│           └── Clear button
│
├── HoverPanel (right side, collapsible)
│   ├── NodeVisibility (4 city toggles)
│   ├── PacketAnimation (on/off + speed slider)
│   ├── ThemeSwitcher (Space / Aurora)
│   ├── AutoRotateToggle
│   ├── CommandHistoryToggle
│   └── Section animations via container-scroll-animation
│
├── ConnectionManager (Zustand actions)
│   ├── WS: ws://localhost:5174/ws/topology (device state 1s)
│   ├── REST: POST /api/device/:id/:action (fire commands)
│   └── Actions: pingDevice, triggerAnomaly, lockdownRoute, etc.

└── NotificationLayer (anime.js toast stack)
    ├── CommandSent (brief confirmation)
    ├── CommandResult (success/failure with data)
    └── T3Disconnected (red flash)
```

## Component Mapping (Reference Components)

| Component | Usage |
|-----------|-------|
| `WorldMap` | Base Three.js map layer from `map.tsx` |
| `RadialOrbitalTimeline` | Orbital ring logic for city node satellite orbits |
| `FlightcnSatelliteOrbits` | Trail rendering adapted for packet paths |
| `ThemeToggleButtons` | All toggle switches in hover panel |
| `ContainerScrollAnimation` | Scroll-reveal for DeviceDetailPanel and CommandHistory |
| `SystemMonitor` | Mini-widget showing aggregate device health |
| `AnimatedHudTargetingUi` | Crosshair/reticle logic for node targeting cursor |
| `ProcessingCard` | Action button cards and device detail panel |

## Zustand Stores

```
store/deviceStore     — device states, link status, metrics (from WS)
store/commandStore    — command history, pending/sent/result states
store/uiStore         — active panel, theme, auto-rotate, packet toggle
store/wsStore         — connection status, reconnect state
```

## 3D Scene Details

- **India Map**: GeoJSON outline rendered as BufferGeometry lines with cyan glow
- **City Nodes**: SphereGeometry + glow sprite + pulsating ring (custom shader)
- **Packet Arcs**: CatmullRomCurve3 between city positions, PointsGeometry along curve, animated via anime.js
- **Starfield**: PointsGeometry with random positions, subtle parallax on camera move
- **Ripple Effect**: Ring geometry that scales up and fades opacity (anime.js)

## Data Flow

```
T3 (port 5174)                            T1 (port 5173)
    │                                          │
    ├── WS /ws/topology ──────────────────────►│  Device state (1s interval)
    │   { devices: [...], links: [...], ... }   │
    │                                          │
    │◄── POST /api/device/:id/:action ────────┤  Commands
    │   { action: "ping", target: "..." }      │
    │                                          │
    │──► Response ────────────────────────────►│  Command result
    │   { success, rtt, ... }                  │
```

## Design Principles

1. **No internet required** — all assets local, no CDN
2. **Real-time first** — WS push for live device state
3. **Command authority** — every action has loading/success/error states
4. **Space-ops aesthetic** — glowing elements, dark theme, Orbitron font
5. **State parity** — shared Zustand pattern; backend mirrors via WS
