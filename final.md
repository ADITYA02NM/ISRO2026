# 🚀 ISRO BAH 2026 — Final Submission Content

> **Team:** Cyber Assassins
> **Challenge 13:** Air-Gapped Predictive Copilot for Secure MPLS Operations
> **College:** Bangalore Institute of Engineering

---

## 📋 PART A: PORTAL FORM TEXT

Copy these directly into the submission portal at [https://bah.isro.gov.in](https://bah.isro.gov.in)

---

### 1. Challenge

```
Challenge 13 — Air-Gapped Predictive Copilot for Secure MPLS Operations
```

---

### 2. Brief about your Idea (max 1024 chars)

```
An autonomous, air-gapped AI NOC Copilot that predicts MPLS/SD-WAN network failures before they impact operations — entirely within a secure offline environment. We simulate a realistic multi-site enterprise network using Containerlab (FRRouting BGP/OSPF/MPLS, IPSec tunnels, TRex traffic generation), collect telemetry via Telegraf→Prometheus→Kafka, and feed it into a multi-model ML ensemble (LSTM + Prophet + Graph Neural Network + XGBoost) that predicts failures with configurable lead-time windows. A fully offline quantized LLM (Qwen3-8B on Ollama) with RAG over internal runbooks answers three critical questions in real time: (Q1) What is likely to fail next — and when? (Q2) Why is risk elevated — which signals contributed? (Q3) What corrective action should be taken before SLA or security impact occurs? A dual 3D WebGL frontend (Devices Control UI + Analytics Dashboard UI, both React Three Fiber + drei + Three.js) provides interactive 3D NOC visualization and real-time telemetry overlays with ECharts and anime.js micro-animations. ALL infrastructure runs locally via Floci (local AWS emulation — no cloud dependency). Every component operates within a verifiable air-gapped boundary, making this suitable for ISRO, government, and regulated environments where data cannot leave the premises.
```

> **Char count:** ~1024 ✓

---

### 3. What problem are you trying to solve? (max 2000 chars)

```
Modern enterprise and government networks rely on SD-WAN deployments running over MPLS underlays. As these networks grow in complexity, operational visibility and response speed become critical — yet conventional NOC tooling remains fundamentally reactive.

The core problem has two dimensions:

1. REACTIVE DETECTION — Threshold-based monitoring systems fire alerts only AFTER performance breaches or failures occur. By the time an operator sees the alarm, service has already degraded, impacting mission-critical operations. There is no predictive capability to foresee failures before they happen.

2. AIR-GAP CONSTRAINTS — Regulated environments (ISRO, defence, government) prohibit cloud-connected AI solutions. Data cannot leave the premises. This eliminates most modern AI-powered network operations tools that rely on cloud ML inference, managed AI services, or external API calls. Operators in these environments are left without intelligent decision support.

The gap is clear: operators in air-gapped networks need predictive, AI-powered assistance that works entirely offline — forecasting failures, explaining root causes, and prescribing corrective actions — without ever connecting to the internet.

Our solution bridges this gap by creating an end-to-end air-gapped network operations platform where:
- A realistic network simulation generates telemetry and fault scenarios for validation
- A multi-model ML ensemble (LSTM + Prophet + GNN + XGBoost) predicts failures with quantified confidence and time-to-impact estimates
- A quantized LLM (Qwen3-8B) running fully offline on consumer GPU hardware with RAG over internal runbooks provides natural-language explanations and recommended actions
- A 3D NOC dashboard visualises real-time topology, telemetry, and predictions
- ALL cloud services are emulated locally via Floci (S3, DynamoDB, Lambda, SQS, KMS)

The entire system is verified by an air-gap integrity scanner that certifies zero outbound network calls at runtime. This makes predictive AI network operations viable for the first time in environments where security requirements have traditionally prevented it.
```

> **Char count:** ~1520 ✓ (under 2000)

---

### 4. Technology Stack being used (max 1024 chars)

```
Network Simulation: Containerlab, FRRouting (BGP/OSPF/MPLS), StrongSwan/WireGuard (IPSec), DPDK/TRex (traffic gen)
Telemetry Pipeline: Telegraf, Prometheus (+ Alertmanager), Apache Kafka, Elasticsearch, Loki
Machine Learning: PyTorch (LSTM), Prophet (seasonal), PyTorch Geometric (GNN), Scikit-learn (Isolation Forest), XGBoost (ensemble fusion), ONNX Runtime (model export)
Offline LLM & RAG: Ollama (inference), Qwen3-8B Q4_K_M (primary model, 6.0 GB VRAM), Qwen3-4B-Thinking Q5_K_M (fallback), ChromaDB (vector store), LangChain (RAG pipeline), SentenceTransformers/all-MiniLM-L6-v2 (embeddings)
Frontend: React 18 + Vite (two separate apps), Three.js + React Three Fiber + drei (3D viz for both UIs), anime.js v4 (micro-interactions), Apache ECharts (analytics overlays), Zustand (state management)
Infrastructure: Floci (local AWS emulation — S3, DynamoDB, Lambda, SQS, KMS), Docker Compose, Local Docker Registry, MinIO (S3 fallback)
Hardware: NVIDIA RTX 4060 Laptop 8GB VRAM, Ryzen 9 8945HS, 15GB RAM
```

> **Char count:** ~900 ✓

---

### 5. Is this your first hackathon? Experience (max 1024 chars)

```
No, this is not our first hackathon. Our team has prior experience participating in and building projects under time-constrained competitive programming and hackathon environments. This experience has taught us the importance of modular architecture, clear interface contracts between components, and iterative validation — all of which we have applied to this project. However, this is our FIRST ISRO hackathon, and we are excited about the opportunity to apply our skills to the unique challenges of air-gapped, security-critical network operations for the Indian space sector.
```

> **Char count:** ~470 ✓

---

## 📑 PART B: PPT SLIDE CONTENT

Fill these into the [ISRO BAH 2026 Idea Submission Template.pptx](https://github.com/ADITYA02NM/ISRO2026/blob/main/%5BPub%5D%20ISRO%20BAH%202026%20_%20Idea%20Submission%20Template.pptx)

---

### SLIDE 1 — Title / Team Info

| Field | Value |
|-------|-------|
| **Team Name** | Cyber Assassins |
| **Problem Statement** | Challenge 13: Air-Gapped Predictive Copilot for Secure MPLS Operations |
| **Team Leader Name** | Aditya Gowda |

---

### SLIDE 2 — Team Members

| Role | Name | College |
|------|------|---------|
| **Team Leader** | Aditya Gowda | Bangalore Institute of Engineering |
| **Team Member 1** | Dontamsetti Tanuhya | Bangalore Institute of Engineering |
| **Team Member 2** | Priyanka Meenkeri | Bangalore Institute of Engineering |
| **Team Member 3** | Shreeraksha H S | Bangalore Institute of Engineering |

---

### SLIDE 3 — Opportunity / USP

**How is this different from existing ideas?**

Existing NOC tools (SolarWinds, PRTG, Nagios, Grafana) are reactive — they alert AFTER a failure. Cloud-based AIOps solutions (Cisco AI Ops, Splunk IT Service Intelligence) require internet connectivity, making them unusable in air-gapped environments. Our solution is the FIRST to combine:

1. Predictive ML (not just reactive thresholds)
2. Offline LLM with RAG (not cloud-dependent AI)
3. Verifiable air-gap compliance
4. Consumer-grade GPU affordability (RTX 4060)

**How will it solve the problem?**

```
Input: Real-time telemetry from MPLS/SD-WAN network
  ↓
ML Ensemble predicts: WHAT will fail, WHEN (time-to-impact), WHY (contributing signals)
  ↓
LLM Copilot generates: Natural language alert + recommended corrective action
  ↓
NOC Dashboard displays: 3D topology view, timeline, confidence scores
  ↓
Operator acts: Pre-emptive reroute / configuration change BEFORE SLA breach
```

**USP (Unique Selling Proposition)**

> **"The first air-gapped predictive AI copilot for MPLS operations that runs entirely on a gaming laptop — no cloud, no internet, no expensive infrastructure."**

---

### SLIDE 4 — Features

**Add the `features_row.png` image here** (shows 6 feature cards side by side)

| # | Feature | Description |
|---|---------|-------------|
| 🔮 | **Predictive Fault Analytics** | LSTM + Prophet + GNN ensemble predicts failures with configurable lead-time |
| 🤖 | **Offline LLM Copilot** | Qwen3-8B running fully locally with RAG over internal runbooks |
| 🌐 | **Network Simulation** | Containerlab multi-site topology with MPLS, BGP, IPSec — realistic ground truth |
| 📊 | **3D NOC Dashboard** | WebGL/Three.js real-time topology with anime.js micro-interactions |
| ⚡ | **Floci Cloud Emulation** | All AWS services emulated locally — zero cloud dependency |
| 🔐 | **Air-Gap Security** | Verifiable integrity scanner certifies zero outbound calls at runtime |

---

### SLIDE 5 — Process Flow Diagram

**Add the `flow_diagram.png` image here**

The flow shows a 3-terminal, 8-step pipeline:

```
MPLS Network Simulation  →  Telemetry Collection (SNMP/gNMI)
       ↓                          ↓
  Fault Injection       →  Feature Engineering Pipeline
                                ↓
                    ML Prediction Engine (LSTM · Prophet · GNN)
                                ↓
                     Anomaly Detection (Isolation Forest)
                                ↓
                     LLM Copilot (Qwen3-8B + RAG)
                                ↓
                    3D NOC Dashboard (Real-time WebSocket)
```

A feedback loop runs from Dashboard back to Fault Injection for automated validation of 7 fault scenarios.

---

### SLIDE 6 — Wireframes / Mock Diagrams

**Add the `wireframe_mock.png` image here**

Shows a 3-terminal system mockup:
- **TERMINAL 1 (Devices UI):** 3D NOC Control Room — interactive device meshes in WebGL, hover info panels, fault injection buttons, lockdown controls
- **TERMINAL 3 (Dashboard UI):** 3D Analytics Dashboard — same 3D room with ECharts analytic overlays, real-time alert feed with severity coloring, AI Copilot Q&A chat panel
- **RIGHT PANEL (Copilot):** AI Chat Interface showing:
  - *"What is likely to fail next?"* → BGP session PE1→PE2 will flap in ~8min (87% confidence)
  - *"Why is risk elevated?"* → Latency drift +8%, BGP route churn detected
  - Chat input bar at bottom

---

### SLIDE 7 — Architecture Diagram

**Add the `arch_diagram.png` image here**

3-terminal layered architecture inside an air-gapped boundary (Devices UI + Backend + Dashboard UI):

```
┌────────────────────── AIR-GAPPED BOUNDARY ──────────────────────┐
│                                                                  │
│  ┌──────────────────┐  ┌────────────────┐  ┌──────────────────┐  │
│  │ Network Simulation│  │ Telemetry      │  │ Fault Injection  │  │
│  │ (Containerlab)    │→ │ Pipeline       │  │ Engine           │  │
│  │ FRR · IPSec · TRex│  │ Telegraf→Kafka │  │ 7 fault types    │  │
│  └──────────────────┘  └───────┬────────┘  └──────────────────┘  │
│                                ↓                                 │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  Predictive ML Engine (LSTM · Prophet · GNN · XGBoost)       │ │
│  │  + Anomaly Detection (Isolation Forest · Graph Anomaly)      │ │
│  └───────────────────────────┬──────────────────────────────────┘ │
│                              ↓                                   │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  LLM Copilot (Qwen3-8B + RAG + ChromaDB + LangChain)        │ │
│  │  + Runbook Knowledge Base                                    │ │
│  └───────────────────────────┬──────────────────────────────────┘ │
│                              ↓                                   │
 │  ┌───────────────────────┐  ┌───────────────────────┐          │
│  │ Devices UI (T1)       │  │ Dashboard UI (T3)     │          │
│  │ R3F + drei + anime.js │  │ R3F + drei + ECharts  │          │
│  │ REST commands          │  │ WS telemetry + alerts │          │
│  └──────────┬────────────┘  └──────────┬────────────┘          │
│             │                           │                       │
│  ┌──────────┴───────────────────────────┴────────────┐          │
│  │ FastAPI Backend (T2) — REST + WebSocket + Qwen3   │          │
│  └──────────────────────┬────────────────────────────┘          │
│                         ↓                                      │
│  ┌──────────────────────────────────────────────────────┐       │
│  │ Floci (Local AWS Emulation) — S3·DynamoDB·KMS·Lambda  │       │
│  └──────────────────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────────────────┘
```

---

### SLIDE 8 — Technologies

| Layer | Technology |
|-------|-----------|
| **Network Simulation** | Containerlab, FRRouting (BGP/OSPF/MPLS), StrongSwan IPSec, TRex traffic generator |
| **Telemetry** | Telegraf, Prometheus + Alertmanager, Apache Kafka, Elasticsearch, Loki |
| **ML Models** | PyTorch (LSTM), Prophet, PyTorch Geometric (GNN), Scikit-learn, XGBoost, ONNX |
| **LLM & RAG** | Ollama, Qwen3-8B (Q4_K_M), Qwen3-4B-Thinking (fallback), ChromaDB, LangChain |
| **Frontend (Devices UI)** | React 18 + Vite, Three.js + R3F + drei, anime.js v4, Zustand |
| **Frontend (Dashboard UI)** | React 18 + Vite, Three.js + R3F + drei, anime.js v4, ECharts, Zustand |
| **Infrastructure** | Floci, Docker Compose, Local Registry, MinIO |
| **Hardware** | NVIDIA RTX 4060 8GB VRAM, Ryzen 9 8945HS, 15GB RAM |

---

### SLIDE 9 — Estimated Implementation Cost

| Item | Cost (INR) | Notes |
|------|-----------|-------|
| **Hardware (Already Owned)** | ₹0 | RTX 4060 Laptop + Ryzen 9 + 15GB RAM — sufficient for full dev |
| **Software (Open Source)** | ₹0 | All tools are free/open-source (Containerlab, FRR, PyTorch, Ollama, etc.) |
| **Cloud Services** | ₹0 | Floci replaces all AWS services locally |
| **Domain / Hosting** | ₹0 | Fully air-gapped — no hosting needed |
| **3D Dashboard Libraries** | ₹0 | Three.js, anime.js, ECharts — all MIT/BSD licensed |
| **LLM Models** | ₹0 | Qwen3-8B is Apache 2.0 licensed, downloaded via Ollama |
| **Total** | **₹0 (Zero)** | Entire project built with free, open-source tools on existing hardware |

---

### SLIDE 10 — Thank You

```
              🙏 Thank You 🙏

     Team Cyber Assassins
     Bangalore Institute of Engineering

     Challenge 13: Air-Gapped Predictive Copilot
     for Secure MPLS Operations

     ISRO Bharatiya Antariksh Hackathon 2026
```

---

## 📎 PART C: SUBMISSION CHECKLIST

- [ ] **Portal Form:** Copy text from PART A into the 5 portal fields
- [ ] **Challenge:** Challenge 13 (select from dropdown)
- [ ] **PPT Deck:** Fill slides using PART B content. Add diagrams:
  - Slide 4: Use `/tmp/features_row.png` or recreate from table
  - Slide 5: Use `/tmp/flow_diagram.png`
  - Slide 6: Use `/tmp/wireframe_mock.png`
  - Slide 7: Use `/tmp/arch_diagram.png`
- [ ] **Convert PPTX to PDF** (File → Export → PDF, or use LibreOffice)
- [ ] **Upload PDF** to portal (max 5 MB)
- [ ] **Deadline:** July 1, 2026 @ 11:59 PM IST

---

## 🔗 Quick Links

- **Project Repository:** https://github.com/ADITYA02NM/ISRO2026
- **Template PPT:** [`[Pub] ISRO BAH 2026 _ Idea Submission Template.pptx`](./[Pub]%20ISRO%20BAH%202026%20_%20Idea%20Submission%20Template.pptx) (in this folder)
- **Project Docs:** [`info/`](./info/) directory
- **Official Portal:** https://bah.isro.gov.in
