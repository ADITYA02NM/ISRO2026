---
created: 2026-06-23
tags: [ps13, dashboard, threejs, animejs, frontend]
---

# NOC Dashboard — `ml/noc-dashboard.html`

**~1,700 lines.** Self-contained ISRO space-themed 3D NOC copilot dashboard. No CDN dependencies — Three.js + anime.js served from local `ml/static/js/`.

## Layout

```
┌─────────────────────────────────────────────────────┐
│  Header Bar: [PS13 logo] [Status dot] [clock]      │
├───────────────────────────┬─────────────────────────┤
│                           │  T2: Right Panel        │
│   3D Orbital Map          │  ┌─Alerts──┬─AI Chat─┐ │
│   (Three.js)              │  │ alert 1 │ chat    │ │
│                           │  │ alert 2 │ msgs    │ │
│                           │  ├──Analytics─────────┤ │
│                           │  │ model status cards  │ │
│                           │  └────────────────────┘ │
├───────────────────────────┴─────────────────────────┤
│  T1: Trigger Panel [Site▼] [Device▼] [Fault▼]       │
│       [Trigger Event] [Random Burst]                │
└─────────────────────────────────────────────────────┘
```

## T1 — Trigger Panel

Bottom control bar for simulating network events:
- **Site selector**: BLR, MUM, CHE, DEL
- **Device selector**: Per-site CE/PE/P devices
- **Fault selector**: 8 fault types (BGP flap, congestion, CRC errors, link fail, LSP break, node crash, route leak, random)
- **Trigger Event**: Sends POST /predict with realistic telemetry for selected fault
- **Random Burst**: Fires 3-5 random events simulating a real fault storm

## T2 — Right Panel (3 tabs)

| Tab | Content |
|-----|---------|
| **Alerts** | Real-time feed of trigger results (severity-coded: 🔴 critical, 🟡 major, 🔵 minor, ⚪ info). Each has expandable details showing ML prediction data |
| **AI Chat** | Natural language Q&A. Sends message to POST /query (RAG + Ollama). Shows streaming response |
| **Analytics** | Live model status cards (7 models, engine type, loaded ✅/❌), health stats from /health endpoint |

## 3D Engine (Three.js)

- **4 orbital planetary sites**: BLR (blue), MUM (green), CHE (orange), DEL (red)
- **Orbiting device moons**: Each site planet has small orbiting spheres for CE/PE/P devices
- **MPLS connection lines**: Glowing lines between sites representing LSPs
- **Auto-orbiting camera**: Slow celestial rotation
- **Hover tooltips**: Raycaster-based hover detection on planets
- **CSS starfield**: Twinkling animated background (canvas overlay)

## Animation Engine (anime.js)

- `loadIn()`: Timeline load animation (header → panels → trigger → 3D)
- `animateAlert()`: Elastic slide-in + pulse highlight for new alerts
- `animateChatMessage()`: Slide from right (user) or left (assistant)
- `particleBurst()`: 12-particle burst on trigger clicks
- `switchTab()`: Smooth fade-out/fade-in for tab transitions
- `animateStatusDot()`: Pulse animation on status changes

## Related

- [[noc-copilot]] — FastAPI backend this dashboard connects to
- [[server-startup]] — How to launch the dashboard
