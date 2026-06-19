# 📚 Resources Index

> **Comprehensive reference of all tools, libraries, data sources, APIs, and learning materials used in this project.**

---

## 🧰 Tools & Technologies

### Network Simulation

| Resource | URL | Purpose |
|----------|-----|---------|
| **Containerlab** | [containerlab.dev](https://containerlab.dev) | Multi-vendor network topology orchestration |
| Containerlab GitHub | [github.com/srl-labs/containerlab](https://github.com/srl-labs/containerlab) | Source code, issues, examples |
| Containerlab Lab Examples | [github.com/srl-labs/containerlab/tree/main/lab-examples](https://github.com/srl-labs/containerlab/tree/main/lab-examples) | Topology examples |
| **FRRouting (FRR)** | [frrouting.org](https://frrouting.org) | Open-source routing stack (BGP, OSPF, ISIS) |
| FRR Docker Images | [hub.docker.com/r/frrouting/frr](https://hub.docker.com/r/frrouting/frr) | Official Docker images |
| FRR Configuration Guide | [docs.frrouting.org](https://docs.frrouting.org) | Configuration reference |
| **StrongSwan** | [strongswan.org](https://strongswan.org) | IPSec VPN implementation |
| StrongSwan Wiki | [wiki.strongswan.org](https://wiki.strongswan.org) | Documentation and examples |
| **WireGuard** | [wireguard.com](https://www.wireguard.com) | Modern, fast VPN tunnel |
| **TRex** | [trex-tgn.cisco.com](https://trex-tgn.cisco.com) | Realistic traffic generation |
| TRex GitHub | [github.com/cisco-system-traffic-generator/trex-core](https://github.com/cisco-system-traffic-generator/trex-core) | Source and documentation |
| **DPDK** | [dpdk.org](https://dpdk.org) | High-performance packet processing |
| **EVE-NG** | [eve-ng.net](https://www.eve-ng.net) | Alternative network emulator (fallback) |
| **GNS3** | [gns3.com](https://www.gns3.com) | Alternative network emulator (fallback) |

### Telemetry & Monitoring

| Resource | URL | Purpose |
|----------|-----|---------|
| **Telegraf** | [github.com/influxdata/telegraf](https://github.com/influxdata/telegraf) | Metrics collection agent |
| Telegraf Plugins | [docs.influxdata.com/telegraf](https://docs.influxdata.com/telegraf) | Input/output plugin docs |
| Telegraf SNMP Plugin | [github.com/influxdata/telegraf/tree/master/plugins/inputs/snmp](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/snmp) | SNMP polling configs |
| **Prometheus** | [prometheus.io](https://prometheus.io) | Time-series database & alerting |
| Prometheus Configuration | [prometheus.io/docs/prometheus/latest](https://prometheus.io/docs/prometheus/latest) | Configuration reference |
| Prometheus Alerting Rules | [prometheus.io/docs/alerting/latest](https://prometheus.io/docs/alerting/latest) | Alert rule documentation |
| **Apache Kafka** | [kafka.apache.org](https://kafka.apache.org) | Stream processing platform |
| Kafka Docker (Confluent) | [hub.docker.com/r/confluentinc/cp-kafka](https://hub.docker.com/r/confluentinc/cp-kafka) | Official Docker images |
| **Elasticsearch** | [elastic.co/elasticsearch](https://www.elastic.co/elasticsearch) | Search & analytics engine |
| Elasticsearch Docker | [docker.elastic.co](https://www.docker.elastic.co) | Official Docker images |
| **Grafana** | [grafana.com](https://grafana.com) | Metrics visualization & dashboards |
| Grafana Dashboard Library | [grafana.com/grafana/dashboards](https://grafana.com/grafana/dashboards) | Community dashboard templates |
| **Loki** | [grafana.com/oss/loki](https://grafana.com/oss/loki) | Log aggregation (air-gap optimized) |

### Machine Learning & Predictive Analytics

| Resource | URL | Purpose |
|----------|-----|---------|
| **PyTorch** | [pytorch.org](https://pytorch.org) | Deep learning framework (LSTM) |
| PyTorch LSTM Docs | [pytorch.org/docs/stable/generated/torch.nn.LSTM.html](https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html) | LSTM API reference |
| **Prophet** | [github.com/facebook/prophet](https://github.com/facebook/prophet) | Time-series forecasting |
| Prophet Documentation | [facebook.github.io/prophet](https://facebook.github.io/prophet) | Usage and tuning guide |
| **PyTorch Geometric** | [pyg.org](https://pyg.org) | Graph Neural Networks |
| PyG Documentation | [pytorch-geometric.readthedocs.io](https://pytorch-geometric.readthedocs.io) | GNN API reference |
| **scikit-learn** | [scikit-learn.org](https://scikit-learn.org) | ML library (Isolation Forest, XGBoost) |
| Isolation Forest | [scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) | Anomaly detection docs |
| **XGBoost** | [xgboost.readthedocs.io](https://xgboost.readthedocs.io) | Gradient boosting framework |
| **Optuna** | [optuna.org](https://optuna.org) | Hyperparameter optimization |
| **ONNX** | [onnx.ai](https://onnx.ai) | Model interchange format |

### Offline LLM & RAG

| Resource | URL | Purpose |
|----------|-----|---------|
| **Qwen3-8B (Q4_K_M)** | [huggingface.co/Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | Primary LLM — full GPU on RTX 4060 (6.0 GB) |
| **Qwen3-4B-Thinking (Q5_K_M)** | [huggingface.co/Qwen/Qwen3-4B-Thinking](https://huggingface.co/Qwen/Qwen3-4B-Thinking) | Backup/faster LLM (3.9 GB, 33 tok/s) |
| **Qwen3-8B GGUF** | [huggingface.co/Qwen/Qwen3-8B-GGUF](https://huggingface.co/Qwen/Qwen3-8B-GGUF) | GGUF quantized version for llama.cpp |
| **Qwen3-4B Instruct** | [huggingface.co/Qwen/Qwen3-4B-Instruct](https://huggingface.co/Qwen/Qwen3-4B-Instruct) | Lightweight variant for rapid experiments |
| **llama.cpp** | [github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) | LLM inference (CPU-optimized) |
| llama.cpp Quantization | [github.com/ggerganov/llama.cpp#quantization](https://github.com/ggerganov/llama.cpp#quantization) | GGUF quantization guide |
| **Ollama** | [ollama.ai](https://ollama.ai) | Easy LLM deployment |
| Ollama Offline Mode | [github.com/ollama/ollama](https://github.com/ollama/ollama) | Offline/local-first inference |
| **LangChain** | [langchain.com](https://langchain.com) | RAG pipeline framework |
| LangChain Python Docs | [python.langchain.com](https://python.langchain.com) | API reference |
| LangChain RAG Guide | [python.langchain.com/docs/use_cases/question_answering](https://python.langchain.com/docs/use_cases/question_answering) | RAG from scratch |
| **ChromaDB** | [trychroma.com](https://www.trychroma.com) | Local vector database |
| ChromaDB Docs | [docs.trychroma.com](https://docs.trychroma.com) | API reference |
| **SentenceTransformers** | [sbert.net](https://sbert.net) | Local embeddings |
| all-MiniLM-L6-v2 | [huggingface.co/sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | Embedding model |

### Frontend

| Resource | URL | Purpose |
|----------|-----|---------|
| **React** | [react.dev](https://react.dev) | UI framework |
| **TypeScript** | [typescriptlang.org](https://www.typescriptlang.org) | Type-safe JavaScript |
| **Vite** | [vitejs.dev](https://vitejs.dev) | Build tool |
| **Three.js** | [threejs.org](https://threejs.org) | 3D graphics library |
| Three.js Documentation | [threejs.org/docs](https://threejs.org/docs) | API reference |
| **React Three Fiber** | [docs.pmnd.rs/react-three-fiber](https://docs.pmnd.rs/react-three-fiber) | React renderer for Three.js |
| **Drei** | [github.com/pmndrs/drei](https://github.com/pmndrs/drei) | R3F utility helpers |
| **anime.js** | [animejs.com](https://animejs.com) | Animation library (v4.4.1+ ESM modular) |
| anime.js Documentation | [animejs.com/documentation](https://animejs.com/documentation) | API reference |
| anime.js GitHub | [github.com/juliangarnier/anime](https://github.com/juliangarnier/anime) | Source code & examples |
| **Apache ECharts** | [echarts.apache.org](https://echarts.apache.org) | Charting library |
| ECharts Examples | [echarts.apache.org/examples](https://echarts.apache.org/examples) | Example gallery |
| **Zustand** | [github.com/pmndrs/zustand](https://github.com/pmndrs/zustand) | State management |
| **Tailwind CSS** | [tailwindcss.com](https://tailwindcss.com) | CSS framework |
| **Radix UI** | [radix-ui.com](https://www.radix-ui.com) | Accessible UI primitives |

### Infrastructure & Cloud Emulation

| Resource | URL | Purpose |
|----------|-----|---------|
| **Floci** | [github.com/floci-io/floci](https://github.com/floci-io/floci) | Free local AWS emulator (replaces LocalStack) |
| Floci Documentation | [floci.io/floci](https://floci.io/floci) | Official docs |
| Floci Docker Hub | [hub.docker.com/r/floci/floci](https://hub.docker.com/r/floci/floci) | Docker images |
| Floci CLI | [github.com/floci-io/floci-cli](https://github.com/floci-io/floci-cli) | CLI tool for Floci |
| Floci Testcontainers (Java) | [github.com/floci-io/testcontainers-floci](https://github.com/floci-io/testcontainers-floci) | Java Testcontainers module |
| Floci Testcontainers (Node) | [npmjs.com/package/@floci/testcontainers](https://www.npmjs.com/package/@floci/testcontainers) | Node.js Testcontainers |
| Floci Testcontainers (Python) | [pypi.org/project/testcontainers-floci](https://pypi.org/project/testcontainers-floci) | Python Testcontainers |
| **MinIO** | [min.io](https://min.io) | S3-compatible storage (fallback if not using Floci S3) |
| **Docker** | [docker.com](https://www.docker.com) | Container runtime |
| **Docker Compose** | [docs.docker.com/compose](https://docs.docker.com/compose) | Multi-container orchestration |

---

## 📊 Datasets & Data Sources

### Generated Data (All within Air Gap)

| Data Type | Source | Format | Volume |
|-----------|--------|--------|--------|
| SNMP interface counters | Simulated devices (FRR) | Prometheus metrics | ~100 metrics/device/min |
| BGP routes/events | FRR bgpd | Structured logs | ~50 events/sec |
| NetFlow flows | TRex / softflowd | IPFIX records | ~1000 flows/sec |
| IPSec tunnel stats | StrongSwan `ipsec stats` | JSON metrics | ~10 tunnels, 1s interval |
| Latency/jitter | TWAMP light / ICMP | Time-series | ~5s interval |
| Syslog events | All devices | RFC 5424 | ~200 messages/min |
| SD-WAN controller telemetry | Simulated controller | gRPC/gNMI | ~10 metrics/sec |
| Fault ground-truth labels | Fault injection engine | CSV annotations | Per-scenario |

### Reference Datasets (External, Used for Model Design)

| Resource | URL | Use |
|----------|-----|------|
| MAWI Working Group Traffic Archive | [mawi.wide.ad.jp/mawi](https://mawi.wide.ad.jp/mawi) | Traffic pattern reference |
| CAIDA Anonymized Internet Traces | [caida.org/data](https://www.caida.org/data) | Anomaly pattern reference |
| BGP Stream (RIPE RIS) | [ris.ripe.net](https://ris.ripe.net) | BGP event pattern reference |
| CICIDS2017 | [unb.ca/cic/datasets/ids-2017.html](https://www.unb.ca/cic/datasets/ids-2017.html) | Network attack reference |

---

## 📚 Learning Resources

### Network & MPLS

| Resource | URL |
|----------|-----|
| MPLS Fundamentals (Cisco Press) | [ciscopress.com/store/mpls-fundamentals](https://www.ciscopress.com/store/mpls-fundamentals) |
| BGP Design & Implementation | [ciscopress.com/store/bgp-design-and-implementation](https://www.ciscopress.com/store/bgp-design-and-implementation) |
| SD-WAN Architecture Overview | [cs.co/sdwan-architecture](https://www.cisco.com/c/en/us/solutions/enterprise-networks/sd-wan/) |
| FRRouting BGP Configuration | [docs.frrouting.org/en/latest/bgp.html](https://docs.frrouting.org/en/latest/bgp.html) |

### Machine Learning

| Resource | URL |
|----------|-----|
| Time-Series Forecasting with LSTM | [machinelearningmastery.com/lstm-for-time-series](https://machinelearningmastery.com/lstm-for-time-series-forecasting/) |
| Prophet Quick Start | [facebook.github.io/prophet/docs/quick_start.html](https://facebook.github.io/prophet/docs/quick_start.html) |
| Graph Neural Networks (TGN) | [towardsdatascience.com/gnn-for-network-analysis](https://towardsdatascience.com/) |
| Network Anomaly Detection with ML | [arxiv.org/abs/2109.10231](https://arxiv.org/abs/2109.10231) |

### LLM & RAG

| Resource | URL |
|----------|-----|
| Building RAG from Scratch (LangChain) | [python.langchain.com/docs/tutorials/rag](https://python.langchain.com/docs/tutorials/rag) |
| llama.cpp Setup Guide | [github.com/ggerganov/llama.cpp#setup](https://github.com/ggerganov/llama.cpp#setup) |
| Qwen3-8B Model Card | [huggingface.co/Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) |
| Quantization Guide (GPTQ vs GGUF) | [huggingface.co/docs/transformers/quantization](https://huggingface.co/docs/transformers/quantization) |

### Containerlab

| Resource | URL |
|----------|-----|
| Containerlab Getting Started | [containerlab.dev/quickstart](https://containerlab.dev/quickstart/) |
| Containerlab FRR Tutorial | [containerlab.dev/manual/topo-design](https://containerlab.dev/manual/topo-design/) |
| Containerlab BGP Lab | [containerlab.dev/lab-examples/bgp](https://containerlab.dev/lab-examples/bgp/) |

### Floci

| Resource | URL |
|----------|-----|
| Floci Quick Start | [floci.io/floci/getting-started/quick-start](https://floci.io/floci/getting-started/quick-start/) |
| Floci Supported Services | [floci.io/floci/services](https://floci.io/floci/services/) |
| Floci Configuration | [floci.io/floci/configuration](https://floci.io/floci/configuration/) |
| Floci Storage Modes | [floci.io/floci/configuration/storage](https://floci.io/floci/configuration/storage/) |
| Floci Migration from LocalStack | [floci.io/floci/getting-started/migrate-from-localstack](https://floci.io/floci/getting-started/migrate-from-localstack/) |

---

## 🔌 API Endpoints

### Local Services (All within Air Gap)

| Service | Endpoint | Port | Auth |
|---------|----------|------|------|
| **Copilot API** | `http://localhost:8000` | 8000 | API key in `SR.md` |
| Copilot Chat | `POST /api/v1/chat` | — | Bearer token |
| Copilot Predict | `GET /api/v1/predictions` | — | Bearer token |
| Copilot Health | `GET /api/v1/health` | — | None (internal) |
| **Floci (AWS)** | `http://localhost:4566` | 4566 | Any non-empty creds |
| Floci S3 API | `s3://localhost:4566` | — | `test/test` |
| Floci DynamoDB | `dynamodb://localhost:4566` | — | `test/test` |
| **Prometheus** | `http://localhost:9090` | 9090 | None (internal) |
| Prometheus Query | `GET /api/v1/query` | — | — |
| Prometheus Rules | `GET /api/v1/rules` | — | — |
| **Grafana** | `http://localhost:3000` | 3000 | `admin/SR.md` |
| **Kafka** | `localhost:9092` | 9092 | None (internal) |
| **Elasticsearch** | `http://localhost:9200` | 9200 | None (internal) |
| **ChromaDB** | `http://localhost:8001` | 8001 | None (internal) |
| **Dashboard (Dev)** | `http://localhost:5173` | 5173 | None (dev) |
| **Ollama** | `http://localhost:11434` | 11434 | None (internal) |

---

## 📦 Offline Packages (Pre-Downloaded for Air Gap)

All Python dependencies are pre-bundled in `docker/python-deps.tar.gz`:

```
# Core ML
torch==2.5.0
torch-geometric==2.6.0
prophet==1.1.6
xgboost==2.1.0
scikit-learn==1.5.0
optuna==4.0.0

# LLM & RAG
langchain==0.3.0
chromadb==0.5.0
sentence-transformers==3.0.0
llama-cpp-python==0.3.0

# Data & Telemetry
pandas==2.2.0
numpy==1.26.0
scipy==1.14.0
kafka-python==2.0.2
prometheus-client==0.20.0

# Web & API
fastapi==0.115.0
uvicorn==0.30.0
websockets==13.0

# Dev & Testing
pytest==8.3.0
black==24.0
mypy==1.11.0
```

> **Node.js dependencies** are pre-bundled in `dashboard/node_modules.tar.gz` — run `npm install` only once before air-gapping.

---

## 📖 Protocol & Standard References

| Standard | Purpose |
|----------|---------|
| **RFC 3031** | MPLS Architecture |
| **RFC 4271** | BGP-4 |
| **RFC 2328** | OSPF v2 |
| **RFC 4301** | IP Security (IPSec) Architecture |
| **RFC 7011** | IPFIX Flow Information Export |
| **RFC 3416** | SNMP Protocol Operations |
| **gNMI** (gRPC Network Mgmt) | Streaming telemetry interface |

---

> *Find more details in [main.md](./main.md) (system design) and [build.md](./build.md) (build instructions).*
