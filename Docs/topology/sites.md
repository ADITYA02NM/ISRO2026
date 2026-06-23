---
created: 2026-06-23
tags: [ps13, topology, sites, network]
---

# Sites — 4-City MPLS SD-WAN

The PS13 topology connects 4 Indian cities in a full mesh.

## Site Map

```
Delhi (DEL) ────────── Bangalore (BLR)
    │                       │
    │                       │
    │                       │
Mumbai (MUM) ────────── Chennai (CHE)
```

## Site Details

| Site | Role | Devices | Region |
|------|------|---------|--------|
| **Bangalore (BLR)** | Primary DC | CE-1, PE-1, P-1 | South India |
| **Mumbai (MUM)** | Secondary DC | CE-2, PE-2, P-2 | West India |
| **Chennai (CHE)** | Branch | CE-3, PE-3 | South India (coastal) |
| **Delhi (DEL)** | Branch | CE-4, PE-4 | North India |

## Cross-Connects

MPLS LSPs between every P/PE pair. IPsec tunnel between Bangalore ↔ Delhi for encrypted inter-DC traffic.

## Dashboard Representation

In [[noc-dashboard]], each site is a 3D orbital planet:
- BLR → Blue (ISRO blue)
- MUM → Green
- CHE → Orange
- DEL → Red

## Related

- [[device-roles]] — CE, PE, P roles explained
- [[network-topology]] — Full topology doc
- [[protocols]] — BGP, OSPF, MPLS, LDP, IPsec
