---
created: 2026-06-23
tags: [ps13, faults, scenarios, ML]
---

# Fault Scenarios — 7 Fault Types

The project simulates 7 network fault scenarios for ML training and dashboard triggering.

## Fault Classes (XGBoost target)

| ID | Fault | Severity | ML Accuracy | Pattern |
|----|-------|----------|-------------|---------|
| 0 | None (normal) | 0 (info) | — | Baseline stable metrics |
| 1 | BGP Flap | 3 (critical) | 99.94% | Latency spikes + BGP prefix drops + route flapping |
| 2 | Congestion | 2 (major) | integrated | Throughput capped at 40% + jitter increases |
| 3 | CRC Errors | 1 (minor) | integrated | Link utilization normal but discards increase |
| 4 | Link Failure | 3 (critical) | integrated | OSPF neighbors drop + latency infinite |
| 5 | LSP Break | 2 (major) | integrated | MPLS LSP count drops + traffic diverts |
| 6 | Node Crash | 3 (critical) | integrated | CPU/memory spike to 100% then zero |
| 7 | Route Leak | 2 (major) | integrated | BGP prefixes spike + latency oscillates |

## Fault Scripts

Located in `scripts/` — ready for Containerlab injection:

| Script | Target | Mechanism |
|--------|--------|-----------|
| `fault-bgp-flap.sh` | Frrouting | `ip route flush` + re-establish BGP sessions |
| `fault-congestion.sh` | TC/netem | `tc qdisc add` with rate limit |
| `fault-crc-errors.sh` | TC | `tc qdisc add` with corrupt/reorder |
| `fault-link-fail.sh` | ip link | `ip link set down` on target interface |
| `fault-lsp-break.sh` | MPLS/LDP | `mpls ldp` session teardown |
| `fault-node-crash.sh` | System | OOM simulation via stress-ng |
| `fault-route-leak.sh` | BGP | Inject more-specific prefixes to hijack traffic |

## Dashboard Trigger

The T1 panel in [[noc-dashboard]] sends POST /predict with TelemetrySnapshot values engineered to match each fault type (e.g., latency=300ms, bgp_prefixes=0 for BGP flap).

## Related

- [[telemetry-schema]] — Data engineered per fault for training
- [[ensemble-predictor]] — XGBoost achieves 99.94% on 8-class classification
- [[network-topology]] — The network these faults target
