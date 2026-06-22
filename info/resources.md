# 📚 Resources Index

## 🖥️ Frontend Stack

### React Three Fiber
- **Framework**: [@react-three/fiber](https://docs.pmnd.rs/react-three-fiber) — React renderer for Three.js
- **Helpers**: [@react-three/drei](https://github.com/pmndrs/drei) — Utility components (OrbitControls, Text, RoundedBox, etc.)
- **Three.js**: [three.js docs](https://threejs.org/docs/) — Core 3D engine
- **JavaScript API**: [three.js manual](https://threejs.org/manual/) — Tutorials and guides

### Animation
- **Anime.js v4**: `npm install animejs@4.4.1`
  - ESM import: `import { animate, scroll, stagger, timeline } from 'animejs'`
  - Must use v4.4.1 specifically (breaking changes from v3)
  - v3 syntax `anime({...})` is deprecated — use named exports instead
  - GitHub: [https://github.com/juliangarnier/anime](https://github.com/juliangarnier/anime)
  - v4 docs are minimal — rely on TypeScript types and examples

### Charts
- **Apache ECharts**: [echarts.apache.org](https://echarts.apache.org/en/option.html) — Chart configuration reference
- **echarts-for-react**: [npm](https://www.npmjs.com/package/echarts-for-react) — React wrapper for ECharts
- **Theme Builder**: [echarts.theme-builder](https://echarts.apache.org/en/theme-builder.html) — Custom chart themes

### Build Tools
- **Vite**: [vite.dev/guide](https://vite.dev/guide/) — Frontend build tool
- **Vite Config**: [vite.dev/config](https://vite.dev/config/) — Configuration reference

---

## ⚙️ Backend Stack

### FastAPI
- **Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) — Main documentation
- **WebSockets**: [fastapi WebSocket docs](https://fastapi.tiangolo.com/advanced/websockets/) — Real-time push
- **Uvicorn**: [uvicorn.org](https://www.uvicorn.org/) — ASGI server

### LLM / ML
- **Ollama**: [ollama.ai](https://ollama.ai/) — Local LLM runner
- **Qwen3**: [github.com/QwenLM/Qwen3](https://github.com/QwenLM/Qwen3) — Model documentation
- **Ollama Python**: [github.com/ollama/ollama-python](https://github.com/ollama/ollama-python) — Python client library

### Infrastructure
- **floci.io**: [floci.io/docs](https://floci.io/docs) — Local AWS emulation (S3, SQS, Lambda)

---

## 🔧 Tools

### JavaScript / Node
- **npm**: [docs.npmjs.com](https://docs.npmjs.com/) — Package manager docs
- **Node.js**: [nodejs.org/docs](https://nodejs.org/docs/latest/api/) — Runtime API

### State Management
- **Zustand**: [github.com/pmndrs/zustand](https://github.com/pmndrs/zustand) — Lightweight state management

### Python
- **Python 3.12+**: [docs.python.org](https://docs.python.org/3/) — Standard library
- **Pydantic**: [docs.pydantic.dev](https://docs.pydantic.dev/) — Data validation (FastAPI models)

### Docker
- **Docker Compose**: [docs.docker.com/compose](https://docs.docker.com/compose/) — Multi-container orchestration

---

## 🎨 Design References

- **R3F + drei examples**: [@react-three/drei examples](https://github.com/pmndrs/drei#readme) — Component usage examples
- **Three.js journey**: [threejs-journey.com](https://threejs-journey.com/) — Tutorial course (paid, high quality)
- **Poimandres ecosystem**: [pmnd.rs](https://pmnd.rs/) — R3F ecosystem (zustand, drei, etc.)

---

## 🐛 Debugging & Performance

- **React DevTools**: [react.dev/learn/react-developer-tools](https://react.dev/learn/react-developer-tools) — Component inspection
- **Three.js Inspector**: Chrome extension for Three.js scene inspection
- **Vite HMR**: Hot Module Replacement for fast iteration
- **FastAPI Swagger**: Available at `http://localhost:8000/docs` — automatic API docs

---

## 📋 Key Versions

| Package | Version | Notes |
|---------|---------|-------|
| react | ^18 | Latest stable |
| vite | ^5 | Fast dev server |
| three | ^0.170 | Latest stable |
| @react-three/fiber | ^8 | R3F core |
| @react-three/drei | ^9 | R3F utilities |
| animejs | 4.4.1 | **Must use v4.4.1** (ESM, named exports) |
| echarts | ^5 | Apache ECharts |
| echarts-for-react | ^3 | React ECharts wrapper |
| zustand | ^5 | State management |
| fastapi | ^0.115 | Python backend |
| uvicorn | ^0.34 | ASGI server |
| qwen3 | 8B / 4B-Thinking | Ollama models |
