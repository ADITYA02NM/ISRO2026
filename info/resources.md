# Stack References — PS13

Key documentation, GitHub repos, and reference material for the PS13 tech stack.

---

## Network Simulation

| Resource | Link | Purpose |
|----------|------|---------|
| Containerlab Docs | [containerlab.dev](https://containerlab.dev) | Topology definition, node types, FRR images |
| FRRouting Docs | [docs.frrouting.org](https://docs.frrouting.org) | BGP, OSPF, MPLS, LDP configuration |
| Containerlab FRR Quickstart | [containerlab.dev/manual/kinds/frr](https://containerlab.dev/manual/kinds/frr) | FRR kind reference for Containerlab |
| StrongSwan Docs | [strongswan.org/documentation](https://www.strongswan.org/documentation.html) | IPsec site-to-site configuration |
| TRex Traffic Generator | [trex-tgn.cisco.com](https://trex-tgn.cisco.com) | Realistic traffic patterns for simulation |
| Containerlab GitHub | [github.com/srl-labs/containerlab](https://github.com/srl-labs/containerlab) | Issue tracker, examples, releases |

### Example Topologies
- [srl-labs/clab-demo](https://github.com/srl-labs/clab-demo) — Reference multi-vendor topologies
- [FRR BGP Lab](https://containerlab.dev/lab-examples/linknet/) — BGP + OSPF + MPLS examples

---

## Telemetry Pipeline

| Resource | Link | Purpose |
|----------|------|---------|
| Prometheus Docs | [prometheus.io/docs](https://prometheus.io/docs) | Time-series DB, scrape configs, alert rules |
| Telegraf Docs | [docs.influxdata.com/telegraf](https://docs.influxdata.com/telegraf) | Metrics collection, output plugins |
| Kafka Docs | [kafka.apache.org/documentation](https://kafka.apache.org/documentation) | Stream processing, topic management |
| Elasticsearch Docs | [elastic.co/guide](https://www.elastic.co/guide) | Log storage, search, Kibana dashboards |
| Prometheus Docker | [hub.docker.com/r/prom/prometheus](https://hub.docker.com/r/prom/prometheus) | Docker image tags, config mounts |

---

## Predictive ML

| Resource | Link | Purpose |
|----------|------|---------|
| PyTorch Docs | [pytorch.org/docs](https://pytorch.org/docs) | LSTM, Autoencoder implementation, ONNX export |
| Prophet Docs | [facebook.github.io/prophet](https://facebook.github.io/prophet) | Trend/seasonality forecasting |
| PyTorch Geometric | [pyg.org](https://pyg.org) | GNN layers, graph data handling |
| XGBoost Docs | [xgboost.readthedocs.io](https://xgboost.readthedocs.io) | Gradient boosting classifier + regressor |
| scikit-learn | [scikit-learn.org](https://scikit-learn.org) | Isolation Forest, train/test split, metrics |
| ONNX Runtime | [onnxruntime.ai/docs](https://onnxruntime.ai/docs) | Cross-platform model inference |
| skl2onnx | [github.com/onnx/sklearn-onnx](https://github.com/onnx/sklearn-onnx) | Convert sklearn models to ONNX |
| ONNX PyTorch Export | [pytorch.org/docs/stable/onnx](https://pytorch.org/docs/stable/onnx.html) | torch.onnx.export reference |

### ML Reference Papers
- "Time Series Anomaly Detection using LSTM Autoencoders" — Malhotra et al. (2016)
- "Prophet: Forecasting at Scale" — Taylor & Letham (2018)
- "Semi-Supervised Classification with Graph Convolutional Networks" — Kipf & Welling (2017)
- "Isolation Forest" — Liu, Ting & Zhou (2008)

---

## LLM + RAG

| Resource | Link | Purpose |
|----------|------|---------|
| Ollama Docs | [ollama.ai/docs](https://ollama.ai/docs) | Model management, API reference, modelfiles |
| Qwen3-8B Model Card | [huggingface.co/Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | Model architecture, prompt format |
| Qwen3-4B-Thinking | [huggingface.co/Qwen/Qwen3-4B-Base](https://huggingface.co/Qwen/Qwen3-4B-Base) | Lightweight reasoning model |
| ChromaDB Docs | [docs.trychroma.com](https://docs.trychroma.com) | Vector store, embedding functions, query |
| LangChain Docs | [python.langchain.com](https://python.langchain.com) | RAG pipeline, text splitting, prompt templates |
| Ollama Python | [github.com/ollama/ollama-python](https://github.com/ollama/ollama-python) | Python client for Ollama API |

### RAG Patterns
- [langchain-ai/rag-from-scratch](https://github.com/langchain-ai/rag-from-scratch) — RAG tutorial series
- [chroma-core/chroma](https://github.com/chroma-core/chroma) — ChromaDB GitHub
- BAAI/bge-small-en-v1.5 — Embedding model (works with ChromaDB)

---

## Frontend

| Resource | Link | Purpose |
|----------|------|---------|
| Three.js Docs | [threejs.org/docs](https://threejs.org/docs) | Core 3D rendering API |
| R3F Docs | [docs.pmnd.rs/react-three-fiber](https://docs.pmnd.rs/react-three-fiber) | React renderer for Three.js |
| @react-three/drei | [github.com/pmndrs/drei](https://github.com/pmndrs/drei) | R3F utilities (OrbitControls, Html, Text) |
| anime.js | [animejs.com](https://animejs.com) | Animation library (traffic, alerts, UI) |
| ECharts | [echarts.apache.org](https://echarts.apache.org) | Charts, gauges, timelines for dashboard |
| Zustand | [github.com/pmndrs/zustand](https://github.com/pmndrs/zustand) | Lightweight state management |
| Vite | [vitejs.dev](https://vitejs.dev) | Build tool, dev server with HMR |

### R3F Patterns
- [pmndrs/gltfjsx](https://github.com/pmndrs/gltfjsx) — If we switch to GLTF models later
- R3F Line component: `<Line>` from drei
- Points + BufferGeometry for traffic particles
- useFrame for animation loop (traffic, glow pulses)

---

## Backend + Infrastructure

| Resource | Link | Purpose |
|----------|------|---------|
| FastAPI Docs | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) | REST + WebSocket, dependency injection |
| FastAPI WebSocket | [fastapi.tiangolo.com/advanced/websocket](https://fastapi.tiangolo.com/advanced/websocket/) | WS broadcast patterns |
| NetworkX Docs | [networkx.org/documentation](https://networkx.org/documentation) | Graph analysis, BFS, centrality |
| floci.io | [floci.io](https://floci.io) | Local AWS emulation (S3, DynamoDB, Lambda) |
| Docker Compose | [docs.docker.com/compose](https://docs.docker.com/compose) | Multi-service orchestration |
| Python asyncio | [docs.python.org/3/library/asyncio](https://docs.python.org/3/library/asyncio.html) | Async task management for pipeline |

---

## Hardware Optimization

| Resource | Link | Purpose |
|----------|------|---------|
| NVIDIA CUDA Docs | [docs.nvidia.com/cuda](https://docs.nvidia.com/cuda) | GPU compute setup |
| Ollama GPU Guide | [ollama.ai/blog/gpu](https://ollama.ai/blog/gpu) | GPU acceleration for Ollama |
| PyTorch CUDA | [pytorch.org/get-started/locally](https://pytorch.org/get-started/locally) | PyTorch CUDA installation |

---

## Learning Paths (if starting fresh)

- **MPLS Fundamentals**: RFC 3031 (MPLS Architecture), RFC 5036 (LDP)
- **BGP Deep Dive**: RFC 4271, "Internet Routing Architectures" — Sam Halabi
- **Containerlab**: Start with [quickstart guide](https://containerlab.dev/quickstart/)
- **Time-Series ML**: PyTorch LSTM tutorial, Prophet quickstart
- **RAG with Ollama**: ChromaDB "getting started" + LangChain RAG tutorial
