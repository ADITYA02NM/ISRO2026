# Frontend 2 — Legacy

This document is retained for historical reference only.

The current frontend does NOT use a separate T2 dashboard. All alert, analytics, and chat functionality is consolidated in the single-page React application served by Express on port 3000.

## What was Frontend 2?

Original plan called for a dedicated "Alert & Solution Dashboard" on port 5174 with ECharts visualizations. This was merged into the unified dashboard in the current architecture.

## Current Equivalent

See `info/frontend.md` for current frontend architecture.

The unified dashboard includes:
- **LeftPanel**: Alert feed + Network Overview + ML ensemble status
- **ChatTab**: AI chat with Ollama LLM (right panel)
- **ControlBar**: Trigger fault + burst + reset (bottom bar)
- These replace the legacy T2 analytics dashboard
