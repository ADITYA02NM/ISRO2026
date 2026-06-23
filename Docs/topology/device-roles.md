---
created: 2026-06-23
tags: [ps13, topology, devices, frr]
---

# Device Roles — CE, PE, P

11 devices across 4 sites, each running **FRRouting** (Free Range Routing) inside Containerlab Docker containers.

## CE (Customer Edge) — 4 devices

BLR-CE-1, MUM-CE-2, CHE-CE-3, DEL-CE-4

Role: Connects customer/end-site to provider network. Runs eBGP toward PE.

Config files: `configs/{site}-ce-*.frr`

## PE (Provider Edge) — 4 devices

BLR-PE-1, MUM-PE-2, CHE-PE-3, DEL-PE-4

Role: Edge of MPLS backbone. Runs iBGP + OSPF + MPLS/LDP. Encapsulates/decapsulates MPLS.

Config files: `configs/{site}-pe-*.frr`

## P (Provider/Core) — 3 devices

BLR-P-1, MUM-P-2, (CHE and DEL share P-1/P-2)

Role: Core MPLS transit routers. Label switching only (no BGP). Runs OSPF + LDP.

Config files: `configs/{site}-p-*.frr`

## FRRouting Services

All FRR Docker images enable:
- `bgpd` — BGP (eBGP on CE, iBGP on PE)
- `ospfd` — OSPF (IGP for MPLS underlay)
- `ldpd` — LDP (label distribution)
- `zebra` — Kernel routing manager

## Related

- [[sites]] — Site layout
- [[protocols]] — Routing protocols
- [[network-topology]] — Full topology doc
