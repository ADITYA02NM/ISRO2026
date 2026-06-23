---
created: 2026-06-23
tags: [ps13, topology, faults, scripts]
---

# Fault Scripts — `scripts/`

7 shell scripts for injecting network faults into Containerlab nodes via `docker exec`.

| Script | Fault | Target | Mechanism |
|--------|-------|--------|-----------|
| `fault-bgp-flap.sh` | BGP Flap | Frrouting `bgpd` | Flush BGP table, reset sessions |
| `fault-congestion.sh` | Congestion | `tc` (netem) | Rate-limit interface to 40% |
| `fault-crc-errors.sh` | CRC Errors | `tc` (netem) | Add corrupt + reorder noise |
| `fault-link-fail.sh` | Link Failure | `ip link` | Bring interface down |
| `fault-lsp-break.sh` | LSP Break | `ldpd` | Tear down MPLS LDP sessions |
| `fault-node-crash.sh` | Node Crash | `stress-ng` | OOM + CPU spike simulation |
| `fault-route-leak.sh` | Route Leak | BGP | Inject more-specific prefixes |

## Usage

```bash
docker exec <container> bash /scripts/fault-bgp-flap.sh
```

Each script lives in `scripts/` and is mounted into Containerlab FRR containers.

## Related

- [[fault-scenarios]] — ML fault classes matched to these scripts
- [[containerlab]] — How to deploy the network to use these
