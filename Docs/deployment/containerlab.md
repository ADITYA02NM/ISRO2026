---
created: 2026-06-23
tags: [ps13, deployment, containerlab, topology]
---

# Containerlab — Network Simulation

**Containerlab 0.76.1** installed at `/usr/local/bin/containerlab`. Launches 11 FRRouting Docker containers in a Clos-like topology.

## Topology File — `topology.clab.yml`

Defines:
- 4 sites (BLR, MUM, CHE, DEL)
- 11 FRR nodes (4 CE, 4 PE, 3 P)
- Links between sites, underlay OSPF, overlay MPLS LDP
- IPsec tunnel (BLR ↔ DEL)

## Deploy

```bash
cd /home/ego/Documents/ISRO2026
containerlab deploy --topo topology.clab.yml
```

## Nodes

| Node | Image | Role |
|------|-------|------|
| BLR-CE-1 | frrouting/frr | Customer Edge |
| BLR-PE-1 | frrouting/frr | Provider Edge |
| BLR-P-1 | frrouting/frr | Core/Provider |
| MUM-CE-2 | frrouting/frr | Customer Edge |
| MUM-PE-2 | frrouting/frr | Provider Edge |
| MUM-P-2 | frrouting/frr | Core/Provider |
| CHE-CE-3 | frrouting/frr | Customer Edge |
| CHE-PE-3 | frrouting/frr | Provider Edge |
| DEL-CE-4 | frrouting/frr | Customer Edge |
| DEL-PE-4 | frrouting/frr | Provider Edge |

## Fault Injection

7 scripts in `scripts/` ready to run inside containers via `docker exec`:

```bash
docker exec $(docker ps -qf name=BLR-PE-1) bash /scripts/fault-bgp-flap.sh
```

## Related

- [[sites]] — Site layout
- [[device-roles]] — CE/PE/P roles
- [[fault-scripts]] — Fault injection scripts
- [[network-topology]] — Architecture doc
