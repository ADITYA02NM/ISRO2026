# 🧠 Learning Path

## 📚 Three.js + R3F Learning

### Three.js Fundamentals (required before R3F)
Three.js is the underlying 3D engine. R3F wraps it in React components, but knowing raw Three.js concepts is essential.

**Core Concepts:**
- **Scene, Camera, Renderer** — the holy trinity of any 3D app
- **Mesh** = Geometry + Material (positioned in 3D space)
- **Geometry** — shapes (BoxGeometry, SphereGeometry, CylinderGeometry) — we use geometric shapes, not imported models
- **Material** — how surfaces look (MeshStandardMaterial, MeshBasicMaterial)
- **Lighting** — ambient, directional, point lights — essential for 3D depth perception
- **Raycaster** — mouse-to-3D intersection detection (hover/click on 3D objects)
- **OrbitControls** — camera manipulation (rotate, zoom, pan)
- **Animation Loop** — requestAnimationFrame → update → render

**Resources:**
- [Three.js Fundamentals](https://threejs.org/manual/#en/fundamentals) — official guide
- [Three.js Interactive Objects](https://threejs.org/manual/#en/picking) — raycasting for click/hover
- [Discover Three.js](https://discoverthreejs.com/) — free book on Three.js

### React Three Fiber
R3F makes Three.js declarative in React — no manual scene graph management.

**Core R3F Concepts:**
- `<Canvas>` — the R3F container (replaces manual renderer setup)
- `<mesh>` — R3F's component for Three.js Mesh — just add geometry + material as children
- **Hooks**: `useFrame`, `useThree`, `useLoader`
- **Events**: `onPointerOver`, `onPointerOut`, `onClick` — React events on 3D objects
- **Auto-dispose**: R3F manages GPU memory — no manual cleanup needed

**Resources:**
- [R3F docs](https://docs.pmnd.rs/react-three-fiber/getting-started/introduction) — official getting started
- [R3F Examples](https://docs.pmnd.rs/react-three-fiber/getting-started/examples) — basic to advanced
- [R3F API Reference](https://docs.pmnd.rs/react-three-fiber/API/hooks) — hooks reference
- [R3F pitfall prevention blog (poimandres)](https://blog.maximeheckel.com/posts/guide-animating-with-react-three-fiber/)

### Drei (R3F Utilities)
Drei provides ready-to-use R3F components that save massive boilerplate:

**Essential drei components for our project:**
- `<OrbitControls>` — camera orbit, zoom, pan
- `<Text>` — 3D text (labels on devices)
- `<RoundedBox>` — boxes with rounded edges
- `<Float>` — floating animation
- `<Html>` — embed HTML in 3D scene (for tooltips/panels)
- `<Environment>` — HDR environment maps
- `<ContactShadows>` — soft shadows under objects
- `<GizmoHelper>` — axis helper in corner

**Resources:**
- [Drei README (all components)](https://github.com/pmndrs/drei#readme) — comprehensive component list
- [Drei Storybook](https://drei.pmnd.rs/) — interactive examples

### Our 3D Device Models
We use **geometric meshes only** (no CAD/GLTF imports):

```
Satellite:   box (body) + cylinder/torus (dish) + cylinder (panel)
Antenna:     cylinder (base) + cone (top) + ring (reflector)
Rover:       box (body) + sphere (wheels) + box (arm)
Module:      rounded box (body) + plane (solar panel)
```

This keeps bundle size minimal and avoids external asset dependencies.

---

## 🎬 Anime.js Learning

**Critical**: We use v4.4.1, which has a completely different API from v3.

### Anime.js v4 Syntax (our version)
```js
// ✅ v4 named exports (CORRECT)
import { animate, scroll, stagger, timeline, inView } from 'animejs'

animate('.element', {
  translateX: 200,
  duration: 1000,
  easing: 'easeOutCubic'
})

// ❌ v3 syntax (DO NOT USE)
import anime from 'animejs'
anime({ targets: '.element', translateX: 200 })  // WRONG for v4
```

### Key Differences: v3 → v4
| v3 | v4 |
|----|----|
| `anime({ targets, ... })` | `animate(targets, params)` |
| `anime.timeline({...})` | `timeline(sequence)` |
| Default import | Named exports only |
| `anime.stagger(...)` | `stagger(...)` |
| Callbacks on object | `begin`, `complete` still work |
| `anime.scroll({...})` | `scroll({...})` |

### Anime.js v4 Resources
- [Anime.js GitHub](https://github.com/juliangarnier/anime) — source code, issues, examples
- **v4 examples are sparse** — rely on:
  - TypeScript type definitions (in node_modules)
  - Official GitHub examples directory
  - Community CodePen examples tagged "animejs"
- **Our use cases**:
  - Panel enter/exit animations (slide, fade)
  - Alert feed flash animations
  - Hover tooltip transitions
  - Status indicator pulsing
  - Loading shimmer effects

---

## 🧠 Qwen3 / LLM Learning

### Qwen3-8B
- Primary LLM for complex tasks (fault analysis, copilot Q&A)
- Runs on Ollama with ~8GB VRAM requirement (our RTX 4060 handles it)
- Context window: 32K tokens

### Qwen3-4B-Thinking
- Fallback model for simpler tasks (runbook templates)
- Faster inference, lower VRAM
- "Thinking" variant has chain-of-thought capability

### Ollama Usage
```bash
# Pull models
ollama pull qwen3:8b
ollama pull qwen3:4b-thinking

# Run interactive
ollama run qwen3:8b

# API (used by our backend)
curl http://localhost:11434/api/generate -d '{
  "model": "qwen3:8b",
  "prompt": "Analyze this telemetry data...",
  "stream": true
}'
```

### Python Integration
```python
import ollama  # pip install ollama

response = ollama.chat(
    model='qwen3:8b',
    messages=[{'role': 'user', 'content': 'Why is sat-3 overheating?'}],
    stream=True
)
for chunk in response:
    print(chunk['message']['content'], end='', flush=True)
```

---

## ⚡ WebSocket Learning

### FastAPI WebSocket
```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws/telemetry")
async def telemetry_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = get_telemetry_snapshot()
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected")
```

### React WebSocket Client (Dashboard UI)
```jsx
import { useEffect, useState } from 'react'

function useWebSocket(url) {
  const [data, setData] = useState(null)
  const [connected, setConnected] = useState(false)
  
  useEffect(() => {
    const ws = new WebSocket(url)
    
    ws.onopen = () => setConnected(true)
    ws.onclose = () => {
      setConnected(false)
      // Auto-reconnect after 3s
      setTimeout(() => /* reconnect logic */, 3000)
    }
    ws.onmessage = (event) => {
      setData(JSON.parse(event.data))
    }
    
    return () => ws.close()
  }, [url])
  
  return { data, connected }
}
```

---

## 📊 ECharts Learning

We use Apache ECharts for analytics panels in the Dashboard UI.

### Basic Usage
```jsx
import ReactECharts from 'echarts-for-react'

const CpuGauge = ({ value }) => (
  <ReactECharts option={{
    series: [{
      type: 'gauge',
      data: [{ value, name: 'CPU %' }],
      min: 0,
      max: 100
    }]
  }} style={{ height: 200 }} />
)
```

### ECharts Concepts
- **Series**: The data visualization type (gauge, bar, line, pie)
- **Axis**: xAxis, yAxis for cartesian charts
- **Grid**: Positioning of chart within container
- **Tooltip**: Hover info on data points
- **VisualMap**: Color mapping for continuous data
- **Responsive**: Charts auto-resize with container

### ECharts Resources
- [ECharts Option Manual](https://echarts.apache.org/en/option.html) — full configuration reference
- [ECharts Gallery](https://echarts.apache.org/examples/en/index.html) — example charts with source
- [echarts-for-react](https://github.com/hustcc/echarts-for-react) — React wrapper

---

## 🎨 Font Resources

- **[Inter](https://rsms.me/inter/)** — UI text (labels, panels, descriptions)
  - Variable font weight support (300–700)
  - Installed system-wide via `apt install fonts-inter`
  
- **[JetBrains Mono](https://www.jetbrains.com/lp/mono/)** — Monospace for telemetry values
  - Ligature support
  - Installed via `apt install fonts-jetbrains-mono`

### Font Check Commands
```bash
fc-list | grep -i inter
fc-list | grep -i "jetbrains mono"
```

---

## 🎯 Quick Reference — Getting Started

### S9A First Steps
```bash
# Create Devices UI project
cd ~/Documents/ISRO2026
npm create vite@latest devices-ui -- --template react
cd devices-ui

# Install 3D deps
npm install three@latest
npm install @react-three/fiber@latest
npm install @react-three/drei@latest
npm install animejs@4.4.1
npm install zustand@latest

# Run
npm run dev
```

### Minimal 3D Room (copy-paste starter)
```jsx
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'

function Scene() {
  return (
    <Canvas camera={{ position: [8, 6, 8] }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} />
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="royalblue" />
      </mesh>
      <OrbitControls />
    </Canvas>
  )
}
```
