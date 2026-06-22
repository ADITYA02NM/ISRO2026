# Learning Path — PS13 Stack

What the solo developer learned (or needed to learn) to build the Air-Gapped Predictive Copilot for Secure MPLS Operations.

---

## 1. Network Simulation (Containerlab + FRRouting)

### Starting Point
Zero experience with container-based network simulation.

### What Was Learned
- Containerlab topology YAML structure (kinds, endpoints, links, binds)
- FRRouting daemon configuration: zebra, bgpd, ospfd, ldpd
- BGP: eBGP multi-hop, iBGP full mesh, route reflectors, prefix limits, hold timers
- OSPF: areas, adjacencies, LSDB synchronization, SPF tuning
- MPLS: LDP label distribution, LSP path computation, label stacking
- IPsec: StrongSwan site-to-site configuration, IKEv2, SA lifecycle
- TRex: traffic profiles, stream generation, latency measurement
- Docker networking: bridge networks, container discovery, port mapping
- Bash automation: clab exec for remote commands, parallel SSH-like control

### Key Challenges
- BGP convergence time with 12+ routers (needed to tune timers)
- MPLS LSP break troubleshooting (label withdrawal scenarios)
- Container resource limits preventing FRR from establishing all peers
- TRex performance on limited CPU cores

---

## 2. Telemetry Pipeline (Telegraf → Prometheus → Kafka → ELK)

### Starting Point
Basic Prometheus knowledge from previous ISRO phases. No Kafka or ELK experience.

### What Was Learned
- Telegraf configuration: prometheus input plugin, output plugins (prometheus, kafka)
- Prometheus: scrape configs with Docker SD, recording rules, alert rules, relabeling
- Kafka: topic partitioning, consumer groups, retention policies, at-least-once delivery
- Elasticsearch: index templates, mapping for metric data, ILM policies
- Kibana: dashboards, lens visualizations, saved searches
- Docker Compose for multi-service pipeline orchestration
- gRPC vs REST for Prometheus remote write

### Key Challenges
- Prometheus cardinally explosion (need to limit label space)
- Kafka consumer offset management (avoiding duplicate processing)
- ELK heap sizing on 15GB RAM machine
- Timestamp alignment between different metric sources

---

## 3. Machine Learning Ensemble (7 Models)

### Starting Point
Basic scikit-learn experience + PyTorch fundamentals from personal projects. No production ML pipeline experience.

### What Was Learned

#### LSTM
- Sequence modeling for time-series (window sizing, normalization, teacher forcing)
- PyTorch LSTM implementation: nn.LSTM, hidden state management, gradient clipping
- Multi-step forecasting (direct vs recursive strategy)
- Synthetic training data generation from TRex patterns

#### Prophet
- Additive model decomposition (trend + seasonality + holidays)
- Changepoint detection for regime shifts
- Uncertainty intervals for prediction bounds

#### GNN (PyTorch Geometric)
- Graph data structures: adjacency matrix, node features, edge features
- GCN layers: message passing, aggregation functions
- Topology-aware prediction: failure propagation through graph
- PyG DataLoader for batch processing

#### XGBoost
- Gradient-boosted decision trees for classification
- Feature importance analysis (SHAP values)
- Hyperparameter tuning (max_depth, learning_rate, n_estimators)
- Multi-class classification for 7 fault types + healthy

#### Anomaly Detection (Isolation Forest + Autoencoder)
- Unsupervised anomaly detection fundamentals
- Isolation Forest: partition-based anomaly scoring
- Autoencoder: reconstruction error as anomaly metric
- Threshold calibration (precision-recall tradeoff)

#### TTI Regressor
- Survival analysis concepts adapted to network failures
- Feature engineering: rate of change of key metrics
- Quantile regression for prediction intervals

#### MLOps
- ONNX export: PyTorch → ONNX, sklearn → ONNX (skl2onnx)
- ONNX Runtime inference in Python
- Model versioning and hot-reloading
- Batch vs streaming inference patterns

### Key Challenges
- GNN training convergence with small synthetic dataset
- ONNX export compatibility (custom PyTorch operations)
- Inference latency with 7 models running sequentially
- Balancing model complexity with RTX 4060 VRAM (8GB)

---

## 4. LLM + RAG (Qwen3-8B + ChromaDB)

### Starting Point
Basic LLM API usage (OpenAI API). No self-hosted LLM or RAG experience.

### What Was Learned
- Ollama: model pulling, GPU acceleration, custom Modelfiles, API integration
- Qwen3-8B: prompt format, context length (32K), system prompt design
- Qwen3-4B-Thinking: activation pattern for reasoning traces
- ChromaDB: collection management, embedding selection, similarity search
- LangChain: RecursiveCharacterTextSplitter, prompt templates, LLM chain
- Structured output: JSON schema validation, retry on parse failure
- RAG evaluation: precision@k, hit rate, response relevance scoring

### Key Challenges
- Qwen3-8B inference speed on RTX 4060 (~20 tokens/s at Q4_K_M quantization)
- VRAM contention between Ollama and ML models (need to unload when not in use)
- ChromaDB embedding quality for network-specific terminology
- Structured JSON output reliability (LLM sometimes produces invalid JSON)
- Prompt template tuning for consistent Q1/Q2/Q3 format

---

## 5. NOC Workflow Automation (NetworkX)

### Starting Point
Basic graph theory knowledge from university. No NetworkX experience.

### What Was Learned
- NetworkX: graph construction, BFS/DFS traversal, centrality metrics
- Blast radius computation: subgraph extraction, distance-bounded BFS
- Alert temporal correlation: sliding window, affinity propagation
- Playbook matching: tag-based recommendation, TF-IDF scoring
- Incident lifecycle: state machine (open → acknowledged → escalated → resolved)

### Key Challenges
- Real-time graph updates during topology changes
- Centrality recalculations on large graphs (optimization needed)
- Temporal window sizing (too small = missed correlations, too large = false positives)

---

## 6. Air-Gap Verification

### Starting Point
General security awareness. No air-gap compliance experience.

### What Was Learned
- DNS leak detection: systemd-resolved analysis, nslookup test patterns
- Process whitelisting: PID namespace isolation, cgroup inspection
- TCP connection audit: `ss` command parsing, `/proc/net/tcp` analysis
- Environment variable security: proxy variable scanning (HTTP_PROXY, etc.)
- Compliance scoring: weighted check aggregation, threshold calibration
- Periodic scanning without performance impact

### Key Challenges
- Distinguishing Docker internal traffic from external connections
- False positives from localhost services (Ollama, Prometheus, Kafka)
- Ensuring scanner itself doesn't produce network connections

---

## 7. 3D Visualization (Three.js + R3F)

### Starting Point
Intermediate React. No Three.js or 3D rendering experience.

### What Was Learned
- Three.js primitives: BoxGeometry, BufferGeometry, PointsMaterial, LineBasicMaterial
- R3F: declarative 3D scene composition, useFrame, useThree
- @react-three/drei: OrbitControls, Html, Text, Edges
- Camera control: lookAt, lerp for smooth transitions
- Object picking: raycasting for click selection
- Particle systems: Points + PointsMaterial for traffic visualization
- Animation loop: useFrame for continuous updates, Clock delta for speed control

### Key Challenges
- R3F performance with 12+ router meshes + traffic particles on integrated GPU
- OrbitControls interference with click-to-select (needed pointer-events tuning)
- Html overlay positioning in 3D space (screen-space projection)
- Mesh scaling for meaningful visual hierarchy

---

## 8. Frontend Technologies

### Starting Point
Experienced with React 18. No anime.js or ECharts experience.

### What Was Learned
- anime.js: timeline animation, SVG morphing, stagger effects
- ECharts: reactive charts, gauge charts, timeline series
- Zustand: middleware (persist, devtools), computed values, slices
- Vite: fast HMR, CSS modules, proxy configuration for API

### Key Challenges
- ECharts performance with real-time streaming data (10+ chart updates/sec)
- anime.js timeline management across component re-renders
- Zustand store synchronization between two independent React apps

---

## 9. Solo Development Practices

### What Worked
- 6-phase plan with clear boundaries (each phase independently verifiable)
- Mock-first development (simulation before real infra)
- Docker Compose for entire pipeline (one-command deploy)
- Pre-built FRR, Prometheus, Kafka images (no custom Dockerfiles needed)
- floci.io for local AWS emulation (no cloud costs)

### What Could Be Improved
- Start ML model training earlier (data generation takes time)
- More realistic TRex traffic profiles (started too simple)
- Earlier ChromaDB embedding quality testing
- Better VRAM management between Ollama and ML models

---

## Learning Resources Used

- **Containerlab**: [containerlab.dev/quickstart](https://containerlab.dev/quickstart/)
- **FRRouting**: [docs.frrouting.org](https://docs.frrouting.org/en/latest/)
- **BGP**: RFC 4271, "Internet Routing Architectures" (Halabi)
- **MPLS**: RFC 3031, RFC 5036
- **PyTorch LSTM**: [pytorch.org/tutorials/beginner/introyt.html](https://pytorch.org/tutorials/beginner/introyt.html)
- **PyG**: [pytorch-geometric.readthedocs.io](https://pytorch-geometric.readthedocs.io)
- **Prophet**: [facebook.github.io/prophet/docs/quick_start](https://facebook.github.io/prophet/docs/quick_start.html)
- **XGBoost**: [xgboost.readthedocs.io/en/stable/python](https://xgboost.readthedocs.io/en/stable/python/)
- **ONNX Export**: [pytorch.org/tutorials/advanced/super_resolution_with_onnxruntime](https://pytorch.org/tutorials/advanced/super_resolution_with_onnxruntime.html)
- **Ollama**: [github.com/ollama/ollama](https://github.com/ollama/ollama)
- **ChromaDB**: [docs.trychroma.com/getting-started](https://docs.trychroma.com/getting-started)
- **LangChain RAG**: [python.langchain.com/docs/tutorials/rag](https://python.langchain.com/docs/tutorials/rag/)
- **Three.js**: [threejs.org/manual](https://threejs.org/manual/)
- **R3F**: [docs.pmnd.rs/react-three-fiber/getting-started/introduction](https://docs.pmnd.rs/react-three-fiber/getting-started/introduction)
- **NetworkX**: [networkx.org/documentation/stable/tutorial](https://networkx.org/documentation/stable/tutorial.html)
- **FastAPI WebSocket**: [fastapi.tiangolo.com/advanced/websocket](https://fastapi.tiangolo.com/advanced/websocket/)
