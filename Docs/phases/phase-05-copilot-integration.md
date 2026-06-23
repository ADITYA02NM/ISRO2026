---
created: 2026-06-23
tags: [ps13, phase-05, copilot, fastapi, dashboard, completed]
status: completed
---

# Phase 5: NOC Copilot Integration

**Status: ✅ COMPLETED — FastAPI server (7 endpoints) + 3D dashboard**

**Goal:** Integrate all 7 ML models + LLM/RAG into a unified FastAPI server with a real-time 3D NOC dashboard.

---

## FastAPI Server — `ml/noc_copilot.py` (531 lines)

### Endpoints

| Method | Path | Function | Input | Output |
|--------|------|----------|-------|--------|
| GET | `/health` | System health + model status | — | models loaded, LLM reachable, RAG count, latency |
| GET | `/models/status` | Per-model status | — | list of {name, loaded, engine, error} |
| POST | `/predict` | Full ML diagnosis | TelemetrySnapshot | fault, anomaly, tti, forecast, autoencoder, lstm, gnn |
| POST | `/explain` | LLM explanation | DiagnosisResult | natural-language analysis |
| POST | `/query` | RAG-Q&A | {question} | LLM answer with context |
| POST | `/rag/ingest` | Trigger RAG ingestion | — | success + doc count |
| GET | `/rag/stats` | RAG document count | — | {count: N} |

### Request/Response Example

**POST /predict:**
```json
{
  "device_id": "PE1-BLR",
  "site": "BLR",
  "device_role": "PE",
  "timestamp": "2026-06-23T14:00:00",
  "cpu_util": 45.2,
  "memory_util": 62.1,
  "bandwidth_util": 38.7,
  "packet_loss_pct": 0.12,
  "latency_ms": 4.23,
  "jitter_ms": 0.89,
  "tcp_retransmits": 1.23,
  "queue_depth": 3,
  "interface_errors": 0.02,
  "bgp_prefix_count": 142,
  "ospf_lsa_count": 34,
  "mpls_lsp_count": 28
}
```

**Response:**
```json
{
  "fault": {"type": "BGP Flap", "confidence": 0.99, "all_probs": {...}},
  "anomaly": {"score": -0.18, "is_anomaly": false},
  "tti": {"hours": 12.4, "severity": 0.45, "fault_prob": 0.62},
  "forecast": {"trend": "stable", "next_24h": [...], "ci": [...]},
  "autoencoder": {"error": 0.031, "is_anomaly": false},
  "lstm": {"prediction_norm": [...], "next_12h": [...]},
  "gnn": {"node_scores": {...}, "fault_prob": 0.12}
}
```

---

## 3D Dashboard — `ml/noc-dashboard.html` (1700+ lines)

### Technology
| Component | Library | Version | Size |
|-----------|---------|---------|------|
| 3D Map | Three.js | r128 (local) | 603 KB |
| Animations | anime.js | 3.2.2 (local) | 17 KB |
| Icons | Font Awesome | 6.x (CDN) | — |
| Backend | Fetch API | — | — |

### Layout
```
┌──────────────────────────────────────────────────┐
│  Header: ISRO PS13 NOC Copilot [Status Dot]      │
├────────────────────────────────┬─────────────────┤
│                                │  T2: Alerts + AI│
│  Three.js 3D Orbital Map       │  ┌─────────────┐│
│  4 planetary sites (BLR/MUM/   │  │ Alert Feed  ││
│  CHE/DEL) with orbiting device │  ├─────────────┤│
│  moons, MPLS connection lines, │  │ AI Chat     ││
│  auto-orbit camera, hover      │  ├─────────────┤│
│  tooltips via raycaster        │  │ Analytics   ││
│                                │  └─────────────┘│
├────────────────────────────────┴─────────────────┤
│  T1: Trigger Panel — Site | Device | Fault        │
│  [Trigger Event] [Random Burst]                   │
└──────────────────────────────────────────────────┘
```

### Features
- **3D Orbital Map**: Sun-centered system with 4 planets (sites), orbiting moons (devices), glowing connection lines
- **T1 Trigger Panel**: Dropdown selectors + Trigger button sends POST /predict, Random Burst fires 3-5 events
- **T2 Alert Feed**: Severity-colored items (red=critical, yellow=warning, blue=info)
- **T2 AI Chat**: POST /query to Ollama via RAG context, markdown-rendered responses
- **T2 Analytics**: Real-time model status polling
- **Auto-Health Poll**: Every 5s checks /health → status dot: green (all good), yellow (partial), red (down)
- **Anime.js**: Load-in anims, elastic alert slides, particle bursts, tab transitions

### Animations (anime.js engine)
| Animation | Trigger |
|-----------|---------|
| Load-in | Page load — header slide-down → panels slide-in → 3D fade-in |
| Alert entry | New alert — elastic slide + pulse glow |
| Chat messages | User: slide right, Assistant: slide left |
| Particle burst | Trigger button click — 12 particles |
| Button pulse | Trigger button — scale + glow ripple |
| Tab switch | T2 tabs — smooth fade-out/fade-in |
| Status dot | Health change — scale pulse |

---

## CORS
Server allows all origins (`add_middleware(CORSMiddleware, allow_origins=["*"])`) for local development.

---

## Startup Sequence
```bash
# Terminal 1: Ollama
ollama serve

# Terminal 2: FastAPI (auto-loads models + RAG)
source ml/venv/bin/activate
uvicorn ml.noc_copilot:app --reload --host 0.0.0.0 --port 8000

# Terminal 3: Dashboard
xdg-open ml/noc-dashboard.html
```

---

## Project Structure
```
ml/
├── noc_copilot.py          # FastAPI server (531 lines)
├── noc-dashboard.html       # 3D HTML dashboard (1700+ lines)
├── static/js/
│   ├── three.min.js         # Three.js (local, 603 KB)
│   └── anime.min.js         # Anime.js (local, 17 KB)
├── rag_pipeline.py          # ChromaDB RAG (330 lines)
├── llm_interface.py         # Ollama wrapper (260 lines)
├── ensemble_predictor.py    # Unified predictor (~1400 lines)
├── vectordb/                # ChromaDB persistent storage
├── models/checkpoints/      # All 7 model files
├── models/onnx/             # ONNX exports
└── data/telemetry.parquet   # Synthetic dataset
```
