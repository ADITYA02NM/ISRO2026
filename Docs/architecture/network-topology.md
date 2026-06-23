---
created: 2026-06-23
tags: [ps13, architecture, network]
---

# Network Topology Architecture

## Overview
4-site MPLS/SD-WAN network running in Containerlab with FRRouting. Each site has distinct roles forming a hub-and-spoke topology with IPsec backup links.

## Topology Map

```
                    ┌──────────────┐
                    │   TRex (ISP) │
                    │  192.168.1.10│
                    └──────┬───────┘
                           │
              ┌────────────┼────────────────────┐
              │            │                     │
         ┌────▼────┐  ┌───▼────┐          ┌─────▼─────┐
         │  P1-BLR │  │ P2-MUM │          │ Internet  │
         │1.1.1.1/32│  │1.1.1.2/32│       │(IPsec Tun)│
         └────┬────┘  └───┬────┘          └─────┬─────┘
              │            │                     │
    ┌─────────┼────────────┼──────────┐          │
    │         │            │          │          │
┌───▼───┐ ┌──▼──┐ ┌───▼───┐ ┌──▼──┐  │   ┌─────▼─────┐
│PE1-BLR│ │CE1- │ │PE1-MUM│ │CE1- │  │   │  PE1-DEL  │
│2.2.2.1│ │ BLR │ │2.2.2.2│ │ MUM │  │   │ 2.2.2.4   │
└───┬───┘ │3.3. │ └───┬───┘ │3.3. │  │   └─────┬─────┘
    │     │3.1  │     │     │3.2  │  │         │
    │     └─────┘     │     └─────┘  │    ┌────▼─────┐
    │                 │              │    │  CE1-DEL │
    │           ┌─────▼─────┐        │    │ 3.3.3.4  │
    │           │  PE1-CHE  │        │    └──────────┘
    │           │ 2.2.2.3   │        │
    │           └─────┬─────┘        │
    │                 │              │
    │           ┌─────▼─────┐        │
    │           │  CE1-CHE  │        │
    │           │ 3.3.3.3   │        │
    │           └───────────┘        │
    │                                │
    └──────── IPsec Tunnel ──────────┘
           (BLR ↔ DEL)
```

## Site Details

| Site | Location | Role | P Router | PE Router | CE Router | Subnet |
|------|----------|------|----------|-----------|-----------|--------|
| Bangalore | HQ (Hub) | Primary data center | P1-BLR (1.1.1.1) | PE1-BLR (2.2.2.1) | CE1-BLR (3.3.3.1) | 10.0.1.0/24 |
| Mumbai | Data Center | Secondary DC | P2-MUM (1.1.1.2) | PE1-MUM (2.2.2.2) | CE1-MUM (3.3.3.2) | 10.0.2.0/24 |
| Chennai | DR Site | Disaster recovery | — | PE1-CHE (2.2.2.3) | CE1-CHE (3.3.3.3) | 10.0.3.0/24 |
| Delhi | Regional | Regional relay | — | PE1-DEL (2.2.2.4) | CE1-DEL (3.3.3.4) | 10.0.4.0/24 |

## Routing Protocols

| Protocol | Area/AS | Purpose |
|----------|---------|---------|
| OSPF | Area 0 | IGP between P/PE routers |
| BGP | AS 65000 | MPLS L3VPN label distribution, customer routes |
| MPLS-LDP | — | Label switching across core |
| IPsec (StrongSwan) | Tunnel | Encrypted backup link BLR↔DEL |

## Fault Scenarios (7 scripts in clab-ps13/scripts/)

| Script | Fault | Duration | Detection Model |
|--------|-------|----------|-----------------|
| `fault_bgp_flap.sh` | BGP session flap | 30s | XGBoost (BGP Flap) |
| `fault_ospf_flapping.sh` | OSPF adjacency flapping | 45s | XGBoost (OSPF Flapping) |
| `fault_mpls_lsp_down.sh` | MPLS LSP failure | 60s | XGBoost (MPLS LSP) |
| `fault_interface_crc.sh` | Interface CRC errors | 90s | IsolationForest/Autoencoder |
| `fault_cpu_spike.sh` | CPU utilization spike | 120s | IsolationForest/LSTM |
| `fault_memory_leak.sh` | Memory leak | 180s | IsolationForest/Autoencoder |
| `fault_queue_drop.sh` | Queue depth overflow | 60s | XGBoost (Queue Drop) |
| `fault_link_flapping.sh` | Link flapping | 45s | XGBoost (Link Flapping) |
