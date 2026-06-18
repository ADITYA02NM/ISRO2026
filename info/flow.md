# 🌊 Software & Technology Flowcharts

> **Visual architecture of the Air-Gapped Predictive Copilot**
>
> All diagrams use Mermaid.js — render them on [mermaid.live](https://mermaid.live) or in any Mermaid-compatible viewer (GitHub, Obsidian, VS Code).

---

## 1. System Architecture Overview

```mermaid
flowchart TB
    subgraph AIRGAP["🚧 Air-Gapped Boundary"]
        direction TB

        subgraph SIM["🌐 Network Simulation"]
            CLAB["Containerlab Topology"]
            FRR["FRRouting BGP/OSPF"]
            IPSEC["IPSec Tunnels"]
            TRAFFIC["TRex Traffic Gen"]
            FAULT["Fault Injection Engine"]
        end

        subgraph TELE["📊 Telemetry Pipeline"]
            TEF["Telegraf<br/>(SNMP · gNMI)"]
            PROM["Prometheus"]
            KAFKA["Kafka Streams"]
            ES["Elasticsearch"]
            LOKI["Loki Logs"]
        end

        subgraph ML["🧠 Predictive Engine"]
            LSTM["LSTM Forecaster"]
            PROPHET["Prophet Model"]
            GNN["Graph Neural Net"]
            ISO["Isolation Forest"]
            XGB["XGBoost Ensemble"]
        end

        subgraph LLM["🤖 Offline LLM Copilot"]
            MISTRAL["Quantized Qwen3-8B"]
            CHROMA["ChromaDB Vector Store"]
            RUNBOOKS["Internal Runbooks"]
            LANGCHAIN["LangChain RAG Pipeline"]
        end

        subgraph UI["🖥️ NOC Dashboard"]
            R3F["React Three Fiber 3D"]
            ANIME["anime.js Micro-interactions"]
            CHARTS["Apache ECharts"]
            GRAFANA["Grafana Panels"]
        end

        subgraph INFRA["☁️ Local Cloud (Floci)"]
            S3["S3 Buckets"]
            DDB["DynamoDB"]
            LAMBDA["Lambda Functions"]
            SQS["SQS Queues"]
            KMS["KMS Keys"]
        end

        SIM --> TELE
        TELE --> ML
        TELE --> LLM
        ML --> LLM
        ML --> UI
        LLM --> UI
        INFRA --> SIM
        INFRA --> TELE
        INFRA --> ML
    end

    OPERATOR["👨‍💻 NOC Operator"] --> UI
    OPERATOR --> LLM
```

---

## 2. Telemetry Pipeline Flow

```mermaid
flowchart LR
    subgraph DEVICES["Simulated Network Devices"]
        CE["CE Routers<br/>(Branch)"]
        PE["PE Routers<br/>(Hub)"]
        P["P Routers<br/>(Core)"]
        SDWAN["SD-WAN Controllers"]
    end

    subgraph COLLECT["Collection Layer"]
        SNMP["SNMP Polling<br/>Telegraf"]
        GNMI["gNMI Streaming<br/>Telegraf"]
        SYSLOG["Syslog Receiver<br/>Rsyslog"]
        NETFLOW["NetFlow/IPFIX<br/>Flow Exporter"]
    end

    subgraph BUFFER["Stream Buffer"]
        KAFKA["Apache Kafka<br/>Topics:<br/>metrics · events · flows · logs"]
    end

    subgraph PROCESS["Processing Layer"]
        STREAM_PRO["Stream Processor<br/>(Kafka Streams)"]
        ALERT["Alert Manager<br/>(Prometheus)"]
        ANOMALY["Real-time Anomaly<br/>(Isolation Forest)"]
    end

    subgraph STORE["Storage Layer"]
        PROM_DB[("Prometheus TSDB")]
        ES_DB[("Elasticsearch")]
        LOKI_DB[("Loki")]
    end

    DEVICES --> SNMP & GNMI & SYSLOG & NETFLOW
    SNMP & GNMI & SYSLOG & NETFLOW --> KAFKA
    KAFKA --> STREAM_PRO & ALERT & ANOMALY
    STREAM_PRO --> PROM_DB & ES_DB & LOKI_DB
    ANOMALY --> PROM_DB
```

---

## 3. ML Training Pipeline

```mermaid
flowchart TB
    subgraph DATA["Data Preparation"]
        RAW["Raw Telemetry<br/>(Prometheus/ES)"]
        LABELS["Fault Labels<br/>(Ground Truth)"]
        FEAT["Feature Engineering<br/>- Rolling windows<br/>- Statistical features<br/>- Fourier transforms<br/>- Graph embeddings"]
        SPLIT["Train/Val/Test Split<br/>70/15/15"]
    end

    subgraph TRAIN["Model Training"]
        LSTM_T["LSTM<br/>· seq_len=128<br/>· 3 layers<br/>· dropout=0.2"]
        PROPHET_T["Prophet<br/>· yearly/weekly<br/>· changepoints<br/>· seasonality"]
        GNN_T["Graph Neural Net<br/>· GCN layers<br/>· topology aware<br/>· node features"]
        ISO_T["Isolation Forest<br/>· n_estimators=200<br/>· max_samples=256"]
    end

    subgraph EVAL["Evaluation"]
        METRICS["Metrics<br/>· Precision/Recall<br/>· F1 Score<br/>· Lead Time<br/>· FAR"]
        ENSEMBLE["Ensemble<br/>(XGBoost Meta-Learner)"]
        THRESHOLD["Threshold Tuning<br/>· Youden's J<br/>· Cost-sensitive"]
    end

    subgraph DEPLOY["Deployment"]
        ONNX["ONNX Export"]
        TRITON["Local Inference<br/>Server"]
        CACHE["Model Cache<br/>(Floci S3)"]
    end

    RAW --> FEAT
    LABELS --> FEAT
    FEAT --> SPLIT
    SPLIT --> LSTM_T & PROPHET_T & GNN_T & ISO_T
    LSTM_T & PROPHET_T & GNN_T & ISO_T --> METRICS
    METRICS --> ENSEMBLE
    ENSEMBLE --> THRESHOLD
    THRESHOLD --> ONNX
    ONNX --> TRITON & CACHE
```

---

## 4. LLM Copilot Inference Flow

```mermaid
sequenceDiagram
    participant Operator as 🧑‍💻 NOC Operator
    participant API as Copilot API (FastAPI)
    participant RAG as RAG Pipeline
    participant VDB as ChromaDB Vector Store
    participant LLM as Quantized Qwen3-8B
    participant CTX as Context Builder
    participant TELE as Live Telemetry

    Operator->>API: "What is likely to fail next?"
    API->>CTX: Fetch current alert state
    CTX->>TELE: Get latest metrics
    TELE-->>CTX: Return top anomalies
    CTX->>VDB: Query similar past incidents
    VDB-->>CTX: Top-k runbook matches
    CTX->>RAG: Build enriched prompt

    Note over RAG: Prompt Structure:<br/>System: NOC copilot persona<br/>Context: Topology + telemetry + runbooks<br/>Query: Operator question

    RAG->>LLM: Forward with context
    LLM-->>RAG: Generated response

    Note over RAG: Response Structure:<br/>🔮 Prediction: Link saturation on PE-1<br/>📊 Confidence: 87%<br/>🎯 Time-to-impact: ~12 minutes<br/>🔍 Root cause: BKUP path BGP flapping<br/>📋 Affected: Site-B, Site-C<br/>🛠️ Action: Shutdown flapping peer

    RAG-->>API: Structured response
    API-->>Operator: Display in NOC Dashboard
```

---

## 5. Fault Injection & Validation Flow

```mermaid
flowchart LR
    subgraph SCENARIOS["Fault Scenarios"]
        CONG["Progressive Congestion<br/>Hub-Spoke Link"]
        FLAP["BGP Route Flap<br/>with Cascade"]
        LINK["MPLS Underlay Failure<br/>Tunnel Degradation"]
        CONF["Controller Misconfig<br/>Policy Drift"]
    end

    subgraph INJECT["Injection Phase"]
        SCRIPT["fault-inject.sh"]
        PARAMS["Parameter Config<br/>· Severity<br/>· Duration<br/>· Ramp-up"]
        EXEC["Execute via<br/>Containerlab/SSH"]
    end

    subgraph DETECT["Detection Phase"]
        LEAD["⏱ Lead Time<br/>Prediction before impact"]
        ACC["🎯 Accuracy<br/>Correct prediction?"]
        CONF_SC["📊 Confidence<br/>Score calibration"]
        EXPL["💬 Explanation<br/>Quality assessment"]
    end

    subgraph RECORD["Recording"]
        GROUND["Ground Truth Label"]
        METRICS_LOG["Metrics Log"]
        COPILOT["Copilot Response"]
        HUMAN["Human Evaluation"]
    end

    SCENARIOS --> SCRIPT
    SCRIPT --> PARAMS
    PARAMS --> EXEC
    EXEC --> DETECT
    DETECT --> LEAD & ACC & CONF_SC & EXPL
    LEAD & ACC & CONF_SC & EXPL --> RECORD
```

---

## 6. Floci Local AWS Integration

```mermaid
flowchart TB
    subgraph FLOCI["Floci (Local AWS Emulation)"]
        direction TB
        GW["API Gateway<br/>:4566"]
        S3_F["S3<br/>Model Artifacts<br/>Runbooks"]
        DDB_F["DynamoDB<br/>Incident Records<br/>Alert State"]
        SQS_F["SQS<br/>Alert Queue<br/>Event Bus"]
        LAMBDA_F["Lambda<br/>Automated Remediation<br/>Playbook Actions"]
        KMS_F["KMS<br/>Local Keys<br/>Air-gapped Crypto"]
    end

    subgraph APP["Application Components"]
        ML_STORE["ML Model Storage"]
        INCIDENT_DB["Incident Database"]
        ALERT_BUS["Alert Event Bus"]
        AUTO_FIX["Auto-Remediation"]
        CRYPTO["Crypto Operations"]
    end

    APP --> GW
    GW --> S3_F & DDB_F & SQS_F & LAMBDA_F & KMS_F
    S3_F --> ML_STORE
    DDB_F --> INCIDENT_DB
    SQS_F --> ALERT_BUS
    LAMBDA_F --> AUTO_FIX
    KMS_F --> CRYPTO

    subgraph CONFIG["Floci Configuration"]
        COMPOSE["compose.yml<br/>docker compose up"]
        ENV["Env Variables:<br/>FLOCI_STORAGE_MODE=persistent<br/>FLOCI_DEFAULT_REGION=us-east-1"]
        INIT["Init Scripts:<br/>S3 bucket creation<br/>DynamoDB tables<br/>SQS queues"]
    end

    CONFIG --> FLOCI
```

---

## 7. Deployment & Orchestration Flow

```mermaid
flowchart TB
    START(["🚀 make up"]) --> DOCKER["Docker Compose<br/>Infrastructure Layer"]

    DOCKER --> FLOCI_S["Floci<br/>Local AWS Emulation"]
    DOCKER --> TELE_S["Telemetry Stack<br/>Telegraf · Prometheus · Kafka · ES"]
    DOCKER --> LLM_S["LLM Service<br/>Ollama · ChromaDB"]

    FLOCI_S --> INIT["Init Scripts<br/>S3 · DynamoDB · SQS · Lambda"]
    INIT --> TOPO["make deploy-topology"]

    TELE_S --> TOPO
    TOPO --> SIM_DEPLOY["Containerlab Deploy<br/>Multi-site Topology"]

    SIM_DEPLOY --> TEL_START["make start-telemetry"]
    TEL_START --> PIPELINE["Telemetry Pipeline Active"]

    PIPELINE --> TRAIN["make train-models"]
    TRAIN --> MODELS["Models Trained & Validated"]

    MODELS --> COPILOT["make start-copilot"]
    COPILOT --> ACTIVE["✅ System Operational"]

    ACTIVE --> DASH["make dashboard<br/>→ http://localhost:3000"]
    ACTIVE --> INJECT["make inject-fault"]
    ACTIVE --> QUERY["make query-copilot"]
```

---

## 8. Data Flow Between Components

```mermaid
flowchart LR
    subgraph RAW["Raw Data Sources"]
        SNMP["SNMP Counters<br/>(ifInOctets, ifOutOctets,<br/>ifErrors)"]
        BGP["BGP Events<br/>(Adjacency, Prefixes,<br/>Flaps)"]
        LATENCY["Latency/Jitter<br/>(ICMP, TWAMP)"]
        FLOW["NetFlow Records<br/>(5-tuple, bytes,<br/>durations)"]
        TUNNEL["Tunnel Stats<br/>(IPSec, GRE,<br/>rekeys)"]
    end

    subgraph FEATURES["Feature Vectors"]
        WINDOW["Time Windows<br/>(5m, 15m, 1h)"]
        STATS["Statistics<br/>(mean, std, p95,<br/>skew, kurtosis)"]
        FREQ["Frequency Domain<br/>(FFT components)"]
        GRAPH["Graph Features<br/>(centrality, degrees,<br/>betweenness)"]
    end

    subgraph MODELS["Model Inputs"]
        LSTM_IN["LSTM<br/>(Sequence: 128 steps)"]
        PROPHET_IN["Prophet<br/>(Timestamps + values)"]
        GNN_IN["GNN<br/>(Adjacency + node features)"]
    end

    subgraph OUTPUT["Model Outputs"]
        PRED["Predictions<br/>· Congestion probability<br/>· Latency drift<br/>· Route stability<br/>· Tunnel health"]
        CONF_SC["Confidence Scores"]
        TTI["Time-to-Impact"]
    end

    SNMP & BGP & LATENCY & FLOW & TUNNEL --> WINDOW
    WINDOW --> STATS & FREQ & GRAPH
    STATS & FREQ --> LSTM_IN & PROPHET_IN
    GRAPH --> GNN_IN
    LSTM_IN & PROPHET_IN & GNN_IN --> PRED
    PRED --> CONF_SC & TTI
```

---

> *All flowcharts rendered with Mermaid.js v11+. Edit and preview at [mermaid.live](https://mermaid.live).*
