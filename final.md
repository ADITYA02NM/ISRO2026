# PS13: Air-Gapped Predictive Copilot for Secure MPLS Operations

## Team Cyber Assassins (4 members, solo development)

---

## 1. Project Summary
An AI-powered NOC copilot that simulates a multi-site enterprise MPLS network, predicts failures using an ensemble of ML models (LSTM, Prophet, GNN, XGBoost, Isolation Forest, Autoencoder, TTI Regressor), and provides natural-language diagnostic assistance via an offline LLM (Qwen3-8B) with Retrieval-Augmented Generation (RAG) over internal runbooks — all running air-gapped on a single RTX 4060 laptop with no cloud dependency.

## 2. Architecture (3-Terminal)

| Terminal | Port | Role | Technology |
|----------|------|------|------------|
| T1 | 5173 | 3D Multi-site MPLS Network Topology View | React 18, Three.js, R3F, @react-three/drei, Zustand |
| T2 | 8000 | Backend: Simulation + Telemetry + ML + LLM + Air-Gap Scanner | FastAPI, PyTorch, Ollama, ChromaDB, Prometheus, Kafka |
| T3 | 5174 | Network Analytics Dashboard + Copilot UI | React 18, anime.js, ECharts, Zustand |

## 3. Build Plan (6 Phases)

| Phase | Deliverable | Key Tech | Timeline |
|-------|-------------|----------|----------|
| 1 | Containerlab 4-site MPLS topology with FRR BGP/OSPF/MPLS/LDP, IPsec tunnels, TRex traffic | Containerlab, FRRouting, StrongSwan, TRex | Days 1-3 |
| 2 | Telemetry pipeline: Telegraf → Prometheus → Kafka → ELK | Telegraf, Prometheus, Kafka, Elasticsearch, Kibana | Days 3-5 |
| 3 | ML ensemble: 6 models + TTI regressor + ONNX export | PyTorch, scikit-learn, XGBoost, Prophet, ONNX | Days 5-8 |
| 4 | Offline LLM copilot: Qwen3-8B + ChromaDB RAG + structured Q1/Q2/Q3 | Ollama, Qwen3-8B, ChromaDB, LangChain | Days 8-10 |
| 5 | NOC workflow: alert correlation, playbook suggestion, incident summaries | NetworkX, FastAPI | Days 10-12 |
| 6 | Air-gap integrity scanner + end-to-end validation | Custom Python scanner | Days 12-14 |

## 4. Key Differentiators
- **True Air-Gap**: DNS leak detection, HTTP proxy validation, process isolation audit — verified at runtime
- **GNN + Topology Awareness**: Graph Neural Network over network topology for failure propagation prediction
- **Structured LLM Output**: Q1 (What) / Q2 (Why) / Q3 (How) framework forces precise diagnostic reasoning
- **Ensemble ML**: 7 models covering time-series, trend, graph, classification, anomaly, and regression
- **Solo-Developed**: Single developer delivering full-stack AI-NOC in 14 days

## 5. Hardware
- GPU: NVIDIA RTX 4060 (8GB VRAM)
- CPU: AMD Ryzen 9 8945HS (16 cores)
- RAM: 15 GB
- All local, no cloud dependency

## 6. Video Demo URL
(To be uploaded after implementation)
