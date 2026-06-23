---
created: 2026-06-23
tags: [ps13, glossary]
---

# 📖 PS13 Glossary

> Plain-English definitions of every technical term. Updated as the project grows.

## A
**Air-Gap** — A computer or network physically disconnected from the internet. No external communication allowed. Our entire project runs air-gapped.
**Autoencoder** — ML model that learns "normal" network patterns. When it sees something that doesn't match, it flags an anomaly (reconstruction error).

## B
**BGP (Border Gateway Protocol)** — The internet's routing protocol. Routers use it to exchange information about which networks they can reach. Like a postal service routing table.

## C
**ChromaDB** — An open-source vector database. Stores document embeddings so the LLM can find relevant troubleshooting guides.
**Containerlab** — A tool that runs virtual network devices as Docker containers. Think of it as "Docker for network equipment."
**Copilot** — AI assistant that watches network telemetry, diagnoses problems, and suggests fixes.

## E
**ESP (Encapsulating Security Payload)** — The encryption part of IPsec. Encrypts the actual data flowing through the tunnel.

## F
**FRRouting (FRR)** — Open-source routing software suite. Supports BGP, OSPF, ISIS, RIP, MPLS, LDP. The Linux equivalent of Cisco IOS.
**Fault Injection** — Deliberately breaking something in the simulated network to test if the monitoring/prediction system detects it.

## G
**GNN (Graph Neural Network)** — ML model that works on graph structures. Understands that if Bangalore's router fails, Mumbai and Chennai are also affected (topology-aware).
**GGUF** — File format for compressed LLM models. Q4_K_M = 4-bit quantization, good quality at half the size.

## I
**IPsec** — Protocol suite for secure encrypted communication over IP networks. Site-to-site VPN between Bangalore and Delhi.
**Isolation Forest** — Anomaly detection algorithm. Finds data points that are "different" from the rest.

## K
**Kafka** — Distributed streaming platform. Like a very reliable message board between systems.

## L
**LDP (Label Distribution Protocol)** — Distributes MPLS labels between routers.
**LSP (Label Switched Path)** — A pre-computed path through an MPLS network. Like a reserved express lane.
**LSTM (Long Short-Term Memory)** — ML model that remembers patterns over time. Good at predicting the next 10 minutes from the last hour.

## M
**MPLS (Multi-Protocol Label Switching)** — Fast forwarding technique using short labels instead of long IP addresses. Like airport baggage tags that tell each handler where to send the bag.

## N
**NOC (Network Operations Center)** — The room where network operators monitor and manage the network.

## O
**Ollama** — Tool for running LLMs locally. Download models and run them offline with a simple CLI.
**OSPF (Open Shortest Path First)** — Interior routing protocol that finds the shortest path between routers within a network.

## P
**PE / P / CE** — Provider Edge (edge router connecting customer), Provider (core router in the middle), Customer Edge (customer's router).
**Prometheus** — Time-series database and monitoring system. Stores metrics like bandwidth, CPU, errors over time.
**Prophet** — Facebook's forecasting library. Finds weekly/daily patterns in time-series data.

## Q
**Q1 / Q2 / Q3** — The three questions: What happened? (Q1), Why did it happen? (Q2), How do we fix it? (Q3).
**Qwen3** — Alibaba's LLM. The 8B variant runs on RTX 4060. Supports Hindi + English.

## R
**RAG (Retrieval-Augmented Generation)** — LLM technique: before answering, retrieve relevant documents from a database, then generate answer based on those docs.
**Route Leak** — Routing misconfiguration where routes leak from one routing domain to another. Can cause traffic to flow through unintended paths.

## T
**TRex** — Realistic traffic generator from Cisco. Simulates real user traffic to exercise the network.
**Telegraf** — Metrics collection agent. Runs on each router, reports stats every 5 seconds.
**TTI Regressor** — Time-To-Incident prediction model. Estimates "how many minutes until this link fails."

## W
**WebSocket** — Technology for real-time two-way communication between server and browser. Used to push telemetry to the operator consoles.

## X
**XGBoost** — Gradient boosted decision trees. Fast, accurate classifier. Used here to classify which type of fault occurred.
