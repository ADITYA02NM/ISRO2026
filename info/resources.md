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

## Dataset Specification

### Synthetic MPLS Telemetry Dataset

Generated by Containerlab simulation with realistic noise injection. Stored in `data/telemetry/`.

| Dataset | Format | Size | Description |
|---------|--------|------|-------------|
| `interface_metrics.csv` | CSV | ~10K rows/day | Per-interface utilization, errors, discards, CRC (5s resolution) |
| `bgp_state.json` | JSON | ~5K rows/day | BGP session state, prefix counts, hold timers, up/down transitions |
| `mpls_labels.json` | JSON | ~3K rows/day | MPLS label operations, LSP state, label bindings per router |
| `ipsec_status.json` | JSON | ~1K rows/day | IPsec SA state, rekey events, tunnel bandwidth |
| `latency_matrix.csv` | CSV | ~2K rows/day | Full-mesh latency measurements between all PE routers |
| `cpu_memory.csv` | CSV | ~10K rows/day | Per-node CPU, memory, process count |
| `fault_labels.csv` | CSV | ~500 rows/day | Ground-truth fault labels for supervised ML |

### Labeled Incident Dataset

Used for training XGBoost classifier and TTI regressor. Stored in `data/labeled/`.

| Field | Type | Example |
|-------|------|---------|
| `timestamp` | ISO8601 | `2026-01-15T14:32:00Z` |
| `device` | string | `PE1_Bangalore` |
| `node_type` | enum | `P`, `PE`, `CE`, `IPsecGW` |
| `site` | string | `Bangalore` |
| `metric_vector` | float[18] | [util, errors, cpu, bgp_prefixes, ...] |
| `fault_type` | enum | `link_failure`, `bgp_flap`, `congestion`, `route_leak`, `crc_errors`, `node_crash`, `lsp_break`, `healthy` |
| `severity` | int (1-5) | 3 |
| `time_to_incident` | int (seconds) | 240 |
| `recovery_action` | string | `bounce_interface` |

### Feature Vector (18 Dimensions)

Used by XGBoost, Isolation Forest, and Autoencoder models:

| Index | Feature | Source | Normalization |
|-------|---------|--------|---------------|
| 0 | Interface utilization % | Telegraf → Prometheus | 0-100 |
| 1 | Error rate (per second) | Telegraf → Prometheus | log scale |
| 2 | CRC error count | Telegraf → Prometheus | log scale |
| 3 | Packet discard rate | Telegraf → Prometheus | log scale |
| 4 | CPU utilization % | Telegraf → Prometheus | 0-100 |
| 5 | Memory utilization % | Telegraf → Prometheus | 0-100 |
| 6 | BGP prefix count | FRR → Telegraf | z-score |
| 7 | BGP session state | FRR → Telegraf | 0=down, 1=flap, 2=up |
| 8 | MPLS label count | FRR → Telegraf | z-score |
| 9 | LSP state | FRR → Telegraf | 0=broken, 1=degraded, 2=ok |
| 10 | Latency to primary peer | ICMP → Prometheus | z-score |
| 11 | Latency to backup peer | ICMP → Prometheus | z-score |
| 12 | Throughput (Mbps) | Telegraf → Prometheus | log scale |
| 13 | Queue depth | Telegraf → Prometheus | log scale |
| 14 | IPsec SA count | StrongSwan → Telegraf | z-score |
| 15 | IPsec rekey count | StrongSwan → Telegraf | rolling window |
| 16 | Process count | host metrics | z-score |
| 17 | Interface flaps/min | FRR → Telegraf | rolling window |

---

## RAG Content — Runbook Library

### Runbook Documents (50+)

Stored in `llm/runbooks/` as markdown, chunked into 512-token segments, embedded with BAAI/bge-small-en-v1.5, indexed in ChromaDB.

**BGP & Routing (12 documents)**

| Document | Topics | Alert Types Matched |
|----------|--------|-------------------|
| `bgp-session-flap.md` | Hold timer mismatch, update delay, route refresh | `bgp_flap` |
| `bgp-convergence.md` | Convergence delay, route propagation, path selection | `bgp_flap`, `route_leak` |
| `bgp-prefix-limits.md` | Max-prefix, soft/hard limits, warning thresholds | `bgp_flap` |
| `bgp-communities.md` | Community stripping, NO_EXPORT, local-pref | `route_leak` |
| `bgp-route-reflector.md` | RR cluster, client configuration, mesh groups | `bgp_flap` |
| `bgp-auth.md` | MD5/TCP-AO authentication, key rollover | `bgp_flap` |
| `bgp-soft-reconfiguration.md` | Soft in/out, route refresh capability | `bgp_flap` |
| `bgp-attributes.md` | AS_PATH, MED, LOCAL_PREF, weight manipulation | `route_leak` |
| `bgp-communities.md` | Standard/extended/large communities | — |
| `bgp-multihop.md` | eBGP multihop, TTL, loopback peering | `bgp_flap` |
| `bgp-nexthop.md` | Next-hop tracking, resolution policy | `bgp_flap` |
| `bgp-addpath.md` | Additional paths, load balancing | — |

**OSPF (6 documents)**

| Document | Topics | Alert Types Matched |
|----------|--------|-------------------|
| `ospf-adjacency.md` | Neighbor states, MTU mismatch, area mismatch | `interface_down` |
| `ospf-lsdb.md` | LSDB corruption, max-age, flooding | `interface_down` |
| `ospf-network-types.md` | Broadcast, point-to-point, NBMA | `interface_down` |
| `ospf-auth.md` | MD5 authentication, key chain, null auth | `interface_down` |
| `ospf-stub-nssa.md` | Stub areas, NSSA, default route injection | — |
| `ospf-route-summarization.md` | ABR/ASBR summarization, cost calculation | — |

**MPLS (6 documents)**

| Document | Topics | Alert Types Matched |
|----------|--------|-------------------|
| `mpls-lsp-break.md` | Label withdrawal, LDP session down, TTL expiry | `lsp_break` |
| `mpls-ldp.md` | LDP discovery, session establishment, label binding | `lsp_break` |
| `mpls-te.md` | Traffic engineering tunnels, bandwidth reservation | `congestion` |
| `mpls-vpn.md` | VRF, route-target, label stacking (inner+outer) | `route_leak` |
| `mpls-frr.md` | Fast reroute, bypass tunnels, protect LSPs | `link_failure` |
| `mpls-php.md` | Penultimate hop popping, explicit null | `lsp_break` |

**IPsec & VPN (5 documents)**

| Document | Topics | Alert Types Matched |
|----------|--------|-------------------|
| `ipsec-sa-mismatch.md` | SA parameters, IKE version mismatch, proposal mismatch | — |
| `ipsec-rekey.md` | Rekey failure, lifetime expiry, DPD timeout | — |
| `ipsec-dead-peer.md` | DPD detection, peer restart, tunnel flap | — |
| `ipsec-nat-traversal.md` | NAT-T, UDP encapsulation, fragmentation | — |
| `ipsec-qos.md` | QoS marking before encryption, DSCP preservation | `congestion` |

**Interface & Hardware (8 documents)**

| Document | Topics | Alert Types Matched |
|----------|--------|-------------------|
| `interface-crc.md` | CRC errors, alignment errors, faulty SFP/cable | `interface_down` |
| `interface-flapping.md` | Link oscillation, speed/duplex mismatch, auto-neg | `interface_down`, `link_failure` |
| `interface-buffer.md` | Buffer drops, queue depth, tail drop | `congestion` |
| `interface-loopback.md` | Loopback detection, spanning-tree, L2 loop | `interface_down` |
| `transceiver-sfp.md` | DOM monitoring, temperature, voltage, bias current | `interface_down` |
| `interface-mtu.md` | MTU mismatch, fragmentation, PMTUD | `link_failure` |
| `interface-errors.md` | Runts, giants, jabber, FCS errors | `interface_down` |
| `interface-utilization.md` | Bandwidth saturation, burst handling, shaping | `congestion` |

**Congestion & QoS (5 documents)**

| Document | Topics | Alert Types Matched |
|----------|--------|-------------------|
| `congestion-detection.md` | Utilization thresholds, queue growth, TCP window | `congestion` |
| `qos-classification.md` | DSCP marking, class-maps, policy-maps | `congestion` |
| `qos-queuing.md` | LLQ, CBWFQ, fair queue, priority queue | `congestion` |
| `qos-shaping.md` | Traffic shaping, policing, token bucket | `congestion` |
| `qos-wred.md` | WRED profiles, drop probability, ECN | `congestion` |

**Device Recovery (4 documents)**

| Document | Topics | Alert Types Matched |
|----------|--------|-------------------|
| `device-crash.md` | Crash analysis, core dump, restart recovery | `node_crash` |
| `device-reload.md` | Planned reload, ISSU, hitless restart | `node_crash` |
| `config-restore.md` | Rollback, backup, commit confirmed | — |
| `software-upgrade.md` | ISSU, image upgrade, compatibility | — |

**General Operations (4 documents)**

| Document | Topics | Alert Types Matched |
|----------|--------|-------------------|
| `incident-response.md` | Triage steps, severity classification, escalation | All |
| `runbook-index.md` | Master index of all runbooks with tag matrix | All |
| `monitoring-baseline.md` | Normal ranges per metric, threshold tuning | All |
| `air-gap-checklist.md` | Air-gap compliance steps, pre-flight checks | All |

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
