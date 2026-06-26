# Frontend 1 — Legacy

This document is retained for historical reference only.

The current frontend does NOT use a separate T1 UI. All frontend functionality is consolidated in the single-page React application served by Express on port 3000.

## What was Frontend 1?

Original plan called for a dedicated "Operator Console" on port 5173 with 3D Three.js router visualizations. This was merged into the unified dashboard in the current architecture.

## Current Equivalent

See `info/frontend.md` for current frontend architecture.

The unified dashboard includes:
- IndiaMap (SVG with clickable cities)
- CityOrbitView (3D R3F orbital scene)
- DeviceInspector (health metrics)
- ControlBar (fault triggers)
- These replace the legacy T1 operator console
