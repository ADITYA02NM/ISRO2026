---
created: 2026-06-23
tags: [ps13, topology, mpls, bgp, ospf, ipsec]
---

# Network Protocols

## BGP (Border Gateway Protocol)

- **CE ↔ PE**: eBGP (customer routes advertised to provider)
- **PE ↔ PE**: iBGP full mesh (MP-BGP for VPNv4 routes)
- Prefix monitoring: `bgp_prefixes` telemetry feature tracks session health

## OSPF (Open Shortest Path First)

- **Underlay IGP** within each site and between P routers
- Area 0 backbone connecting all P and PE routers
- OSPF neighbor count tracked as `ospf_neighbors` telemetry feature

## MPLS + LDP

- **Provider core**: MPLS label switching between P and PE
- **LDP**: Label distribution protocol auto-assigns labels
- LSP count tracked as `mpls_lsp_count` telemetry feature
- MPLS enables traffic engineering and VPN separation

## IPsec

- **Bangalore ↔ Delhi**: Encrypted tunnel for inter-DC traffic
- Protects MPLS-over-internet traffic between the two primary sites
- Not monitored in telemetry (assumed always-up)

## Related

- [[sites]] — Where these protocols run
- [[device-roles]] — Which routers run which protocols
- [[network-topology]] — Full topology
