# Data Flow Sequences — PS13

Network simulation → telemetry → ML prediction → LLM analysis → dashboard visualization.

---

## Core Pipeline

```
[Containerlab]                  [Telegraf]                    [Prometheus]
 FRR router nodes    ───►       agents scrape     ───►       TSDB + alert rules
 (5s metrics)                   per-node metrics              (retention: 24h)
      │                                                              │
      │                                                              │
      │                                                              ▼
      │                                                         [Kafka Broker]
      │                                                       telemetry.metrics
      │                                                       telemetry.alerts
      │                                                       telemetry.events
      │                                                              │
      │                                                ┌─────────────┼─────────────┐
      │                                                ▼             ▼             ▼
      │                                          [ML Engine]  [ELK Stack]   [Backend]
      │                                          batch +       log search   WS push
      │                                          event-driven  & archive    to dashboards
      ▼                                                │
 [Backend]                                              │
 orchestrator                                          ▼
 (start/stop/                                    [LLM Copilot]
  reset/inject)                                 Qwen3-8B + RAG
      │                                         structured Q1/Q2/Q3
      │                                                │
      ▼                                                ▼
 [Network Topology UI]                    [Analytics Dashboard]
 REST poll + WS live                    WS push predictions + alerts + copilot
```

---

## Startup Sequence

```
1. Start Containerlab topology
   └─► FRR nodes boot (4 sites, 12+ routers)
   └─► BGP/OSPF/MPLS converge (~30s)
   └─► IPsec tunnels establish
   └─► TRex traffic generator starts (background load)

2. Start Telemetry Pipeline
   └─► Telegraf agents auto-discover containers
   └─► Prometheus begins scraping (5s interval)
   └─► Kafka topics created (metrics, alerts, events)
   └─► Elasticsearch index templates applied

3. Start ML Engine
   └─► Load 7 models from ONNX
   └─► Subscribe to Kafka telemetry.metrics topic
   └─► Run initial batch inference on Prometheus data
   └─► Begin event-driven inference on Kafka stream

4. Start LLM Copilot
   └─► Verify Ollama running + Qwen3-8B loaded
   └─► Initialize ChromaDB with 50+ runbook documents
   └─► RAG pipeline ready for queries

5. Start Backend API + WebSocket servers
   └─► T1 connects: initial REST poll + WS /ws/topology
   └─► T3 connects: WS /ws/ml + /ws/alerts

6. Dashboard live
   └─► ML predictions start flowing (every 30s batch)
   └─► Alert correlation engine active
   └─► Copilot ready for diagnostic queries
```

---

## Simulation → Topology View Data Flow

```
User requests state (initial load):
T1 ──GET /api/simulation/state──► Backend
    ◄── JSON: sites, routers, links, faults, bgpPeers, mplsLsp── T1

Live updates (WebSocket push):
Containerlab ──(state change)──► Backend ──WS /ws/topology──► T1
  • Link status change (up→down, down→up)
  • BGP session state (established→idle, idle→established)
  • Interface utilization crossing threshold
  • Fault injection confirmation
  • TRex traffic statistics update

User injects fault:
T1 ──POST /api/simulation/fault { type: "bgp-flap", target: "PE2" }──► Backend
    └─► Containerlab: execute fault script
    └─► FRR: BGP session reset on PE2
    └─► WS broadcast: topology update + alert
    ◄── 200 OK + fault_id ── T1
```

---

## Telemetry → ML Pipeline

```
Batch inference (every 30s):
Prometheus ──(query range metrics)──► ML Engine
  • Interface counters (ifInOctets, ifOutOctets, ifInErrors, ifOutErrors)
  • BGP state (bgpPeerState, bgpPeerPrefixes, bgpPeerUpdates)
  • CPU/memory per router node
  • MPLS LSP counters (lspInPackets, lspOutPackets, lspDropped)
  │
  ├──► LSTM: predict next 10min interface utilization
  ├──► Prophet: trend/seasonality decomposition
  ├──► GNN: failure propagation likelihood per node
  ├──► XGBoost: fault type classification
  ├──► Isolation Forest: anomaly score per metric stream
  ├──► Autoencoder: reconstruction error per node
  └──► TTI Regressor: minutes remaining before predicted incident
  │
  └──► Results → Kafka telemetry.predictions topic → WS push to T3

Event-driven inference (on fault/alert):
Kafka telemetry.alerts ──► ML Engine
  • Prometheus alert firing (e.g., LinkUtilization > 90%)
  • Trigger immediate full ensemble inference
  • Compare pre-fault vs post-fault metrics
  • Generate delta analysis
  └──► Send priority prediction to LLM Copilot for diagnosis
```

---

## ML → LLM Copilot Flow

```
Trigger condition:
  • Prediction confidence > 0.8 AND failure probability > 0.5
  • OR alert firing (severity >= warning)
  • OR user explicitly queries copilot

If triggered:
1. ML Engine sends structured context to LLM Copilot:
   {
     "trigger": "prediction|alert|query",
     "device": "PE2",
     "metric": "interface_utilization",
     "value": 94.2,
     "prediction": {
       "model": "lstm",
       "confidence": 0.87,
       "forecast": "critical in 12.3 minutes"
     },
     "related_alerts": [
       {"rule": "LinkUtilizationHigh", "severity": "warning", "since": "2026-06-22T10:23:00Z"}
     ]
   }

2. LLM Copilot queries ChromaDB RAG:
   └─► Vector search: "BGP session flap root cause"
   └─► Retrieved: 3 runbook documents (scores: 0.92, 0.85, 0.74)

3. RAG context + telemetry data → Qwen3-8B prompt:
   └─► Generate structured answer:
   {
     "Q1_What": {
       "failure_type": "bgp_session_flap",
       "severity": "critical",
       "affected_devices": ["PE2", "CE2"],
       "symptoms": ["bgp state idle", "route withdrawal", "traffic drop 40%"]
     },
     "Q2_Why": {
       "root_cause": "BGP hold timer expired (keepalive missed)",
       "evidence": [
         "Last keepalive received 95s ago (hold timer: 90s)",
         "Interface errors on PE2-Gi0/0/1: 247 CRC errors in last 5min",
         "CPU spike on PE2: 78% at time of failure"
       ],
       "confidence": "high"
     },
     "Q3_How": {
       "remediation_steps": [
         "1. Clear BGP session on PE2: clear ip bgp *",
         "2. Check interface errors: show interface gi0/0/1",
         "3. Replace faulty SFP if errors persist",
         "4. Verify route convergence: show ip bgp summary"
       ],
       "escalation_path": "L2 NOC → L3 Network Engineering if SFP replacement needed",
       "estimated_rto": "5 minutes"
     }
   }

4. Response streamed via WS /ws/copilot → T3 Dashboard
```

---

## Alert Correlation Flow

```
1. Alerts generated by Prometheus or ML Engine
   └──► Sent to Kafka telemetry.alerts topic

2. Backend Alert Correlator (NetworkX) processes:
   └─► Build graph from topology (nodes = devices, edges = links)
   └─► For each alert, compute:
       • Affected nodes (direct + blast radius via BFS)
       • Centrality of affected nodes (betweenness, degree)
       • Temporal proximity to other alerts (within 5min window)
   └─► Group alerts sharing same blast radius + temporal window

3. Correlated incident:
   {
     "incident_id": "INC-20260622-003",
     "severity": "critical",
     "root_cause": "P2 Core Router Crash",
     "alerts": [3 correlated alerts],
     "affected_nodes": ["P2", "PE2", "PE1"],
     "blast_radius": "Bangalore-Mumbai-Chennai triangle",
     "network_centrality_impact": 0.72,
     "timestamp": "2026-06-22T14:30:00Z",
     "recommended_playbook": "PB-CORE-RECOVERY-01"
   }

4. Incident → WS /ws/alerts → T3 Dashboard
5. Incident → LLM Copilot (if severity >= warning) for analysis
```

---

## Air-Gap Integrity Scan Flow

```
Trigger: Every 60s (configurable) OR on demand via API

1. DNS Leak Check:
   └──► Attempt DNS resolution for known external domains
   └──► All must return NXDOMAIN or timeout (no external DNS configured)
   └──► Check /etc/resolv.conf for non-local entries

2. HTTP Proxy Check:
   └──► Check env vars: HTTP_PROXY, HTTPS_PROXY, NO_PROXY
   └──► Verify no proxy configured
   └──► Attempt HTTP GET to external URL → must fail/block

3. Process Audit:
   └──► List running processes
   └──► Whitelist: Containerlab, FRR, Prometheus, Kafka, Elasticsearch,
        Telegraf, Ollama, Python (FastAPI), Node (frontends)
   └──► Flag any non-whitelisted process with network capability

4. Data Flow Verification:
   └──► Check tcp/udp connections (ss -tuanp)
   └──► Verify no connections to external IPs
   └──► All connections must be localhost or Docker bridge network

5. Result:
   {
     "status": "compliant|warning|violation",
     "score": 98,
     "checks": {
       "dns_leak": {"status": "pass", "detail": "No external DNS queries"},
       "http_proxy": {"status": "pass", "detail": "No proxy configured"},
       "process_audit": {"status": "pass", "detail": "All processes whitelisted"},
       "data_flow": {"status": "pass", "detail": "No external connections"}
     },
     "last_scan": "2026-06-22T14:35:00Z",
     "violations": []
   }

6. Result → WS /ws/airgap → T3 Dashboard
```

---

## Complete Incident Lifecycle (Example)

```
Time    Event                                               Component
────    ─────                                               ─────────
T+0s    TRex burst simulation starts                        Containerlab
T+5s    Link utilization on P1-PE1 crosses 85%              Telegraf → Prometheus
T+30s   LSTM predicts 98% utilization in 8 minutes          ML Engine
T+31s   Prophet confirms upward trend (p < 0.01)            ML Engine
T+32s   Ensemble: failure probability = 0.76                ML Engine
T+33s   TTI: 7.5 minutes remaining                          ML Engine
T+34s   Autoencoder: reconstruction error spike on P1       ML Engine
T+35s   Priority prediction sent to LLM Copilot             ML Engine
T+36s   ChromaDB RAG: retrieved 2 runbook docs              LLM Copilot
T+37s   Qwen3-8B generates Q1/Q2/Q3 structured answer      LLM Copilot
T+38s   Dashboard receives prediction + copilot answer      WS push to T3
T+40s   Alert: LinkUtilizationCritical (P1-PE1)             Prometheus AlertManager
T+41s   NetworkX: correlate with P1 CPU alert               Backend Correlator
T+42s   Incident created: P1 congestion event               Backend Correlator
T+43s   Playbook suggested: PB-CONGESTION-REROUTE-01        Backend Correlator
T+44s   T3 Dashboard: all panels updated                    WebSocket push
T+60s   Air-gap scan: compliant (score: 100)                Air-Gap Scanner
──
T+8min  LSTM: utilization hit 97%, interface flapping       ML Engine (event-driven)
T+8min  Incident escalated, playbook dispatched to T1       Backend → WS
T+9min  User acknowledges + executes playbook from T3       User action
T+10min Fault resolves, BGP reconverges                     Containerlab
T+10min Dashboard clears alert, logs incident               WS push + ELK
```

---

## REST API Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/simulation/state | Current topology + fault state |
| POST | /api/simulation/fault | Inject fault scenario |
| POST | /api/simulation/reset | Reset to healthy state |
| GET | /api/telemetry/metrics | Prometheus metrics snapshot |
| GET | /api/telemetry/topology | Topology link/device metrics |
| GET | /api/ml/predictions | Latest ensemble predictions |
| POST | /api/ml/query | Ad-hoc inference on custom data |
| POST | /api/copilot/query | Ask LLM (returns Q1/Q2/Q3) |
| GET | /api/copilot/context | RAG context sources metadata |
| GET | /api/workflow/alerts | Correlated alert groups |
| POST | /api/workflow/playbook | Suggest playbook for incident |
| GET | /api/airgap/status | Compliance scan result |
| POST | /api/airgap/scan | Trigger immediate scan |

## WebSocket Topics

| Topic | Push Content | Frequency |
|-------|-------------|-----------|
| /ws/topology | Topology state deltas | On change + 5s heartbeat |
| /ws/ml | ML predictions + TTI updates | Every 30s + event-driven |
| /ws/alerts | New/correlated alerts | On alert firing |
| /ws/copilot | LLM structured responses | On query + on alert-triggered analysis |
| /ws/airgap | Compliance status | Every 60s |
