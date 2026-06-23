---
created: 2026-06-23
tags: [ps13, phase-01, network-simulation, completed]
status: completed
---

# Phase 1: Network Simulation

**Status: ✅ COMPLETED**

**Goal:** Build and verify a realistic multi-site MPLS/SD-WAN network using Containerlab + FRRouting.

**Duration:** Days 1-3 (completed 2026-06-23)

---

## Topology: 4 Sites — 10 FRR Routers + TRex

| Site | Role | P Router | PE Router | CE Router |
|------|------|----------|-----------|-----------|
| Bangalore | HQ (Hub) | P1 | PE1-BLR (2.2.2.1) | CE1-BLR (3.3.3.1) |
| Mumbai | Data Center | P2 | PE1-MUM (2.2.2.2) | CE1-MUM (3.3.3.2) |
| Chennai | Disaster Recovery | — | PE1-CHE (2.2.2.3) | CE1-CHE (3.3.3.3) |
| Delhi | Regional Relay | — | PE1-DEL (2.2.2.4) | CE1-DEL (3.3.3.4) |

### Router Roles

| Type | Count | Loopback | AS | Function |
|------|-------|----------|----|----------|
| P | 2 | 1.1.1.1-2/32 | 65000 | Core backbone — MPLS switching only |
| PE | 4 | 2.2.2.1-4/32 | 65001 | Provider Edge — MPLS ingress/egress, iBGP full mesh |
| CE | 4 | 3.3.3.1-4/32 | 65101-4 | Customer Edge — eBGP to PE |

---

## Complete IP Allocation

### Core Backbone Links (10.0.0.0/8 — OSPF area 0.0.0.0)

| Link | Subnet | Endpoint A | Endpoint B |
|------|--------|------------|------------|
| P1 ↔ P2 | 10.0.1.0/30 | P1 eth1: .1 | P2 eth1: .2 |
| P1 ↔ PE1-CHE | 10.0.2.0/30 | P1 eth2: .1 | PE1-CHE eth1: .2 |
| P1 ↔ PE1-DEL | 10.0.3.0/30 | P1 eth3: .1 | PE1-DEL eth1: .2 |
| P1 ↔ PE1-BLR | 10.0.4.0/30 | PE1-BLR eth1: .1 | P1 eth4: .2 |
| P2 ↔ PE1-CHE | 10.0.5.0/30 | P2 eth2: .1 | PE1-CHE eth2: .2 |
| P2 ↔ PE1-MUM | 10.0.6.0/30 | PE1-MUM eth1: .1 | P2 eth3: .2 |

### Customer Edge Links (192.168.x.0/30 — eBGP between PE/CE)

| Site | Subnet | PE IP | CE IP |
|------|--------|-------|-------|
| Bangalore | 192.168.1.0/30 | PE1-BLR eth2: .1 | CE1-BLR eth1: .2 |
| Mumbai | 192.168.2.0/30 | PE1-MUM eth2: .1 | CE1-MUM eth1: .2 |
| Chennai | 192.168.3.0/30 | PE1-CHE eth3: .1 | CE1-CHE eth1: .2 |
| Delhi | 192.168.4.0/30 | PE1-DEL eth2: .1 | CE1-DEL eth1: .2 |

### TRex Traffic Generator

| Link | Subnet | CE IP | TRex IP |
|------|--------|-------|---------|
| TRex ↔ CE1-BLR | 192.168.10.0/30 | CE1-BLR eth2: .1 | TRex eth1: .2 |

### IPsec VPN (Bangalore ↔ Delhi)

| Tunnel | Subnet | PE1-BLR | PE1-DEL |
|--------|--------|---------|---------|
| VTI | 172.16.0.0/30 | tunnel1: .1 (stub) | tunnel1: .2 (stub) |

### Management Network

| Subnet | Gateway |
|--------|---------|
| 172.20.0.0/24 | Containerlab mgmt bridge |

| Node | Mgmt IP |
|------|---------|
| CE1-BLR | 172.20.0.10 |
| PE1-BLR | 172.20.0.11 |
| P1 | 172.20.0.12 |
| CE1-MUM | 172.20.0.20 |
| PE1-MUM | 172.20.0.21 |
| P2 | 172.20.0.22 |
| CE1-CHE | 172.20.0.30 |
| PE1-CHE | 172.20.0.31 |
| CE1-DEL | 172.20.0.40 |
| PE1-DEL | 172.20.0.41 |
| TRex | 172.20.0.100 |

---

## Routing Protocols

### OSPF (IGP — Backbone Area 0.0.0.0)
- All core-facing interfaces on P1, P2, PE1-BLR, PE1-MUM, PE1-CHE, PE1-DEL
- Loopbacks advertised for LDP transport-address and BGP update-source
- **Not enabled on CE routers** — CEs only run eBGP to their PE

### BGP
- **AS 65000** — P routers (iBGP between P1 ↔ P2, loopback-to-loopback)
- **AS 65001** — PE routers (iBGP full mesh between all 4 PEs, loopback-to-loopback)
  - Loopback routes (2.2.2.x/32) exchanged with next-hop-self
  - CE routes tagged with community 65001:100 on ingress
- **AS 65101–65104** — CE routers (eBGP to connected PE)
  - Each CE advertises its /32 loopback (3.3.3.x/32)
  - CEs receive PE loopbacks via route-map filter

### MPLS + LDP
- Enabled on all core-facing interfaces (P↔P, P↔PE)
- **Not enabled on CE-facing interfaces** — CEs are MPLS-unaware
- Labels distributed via LDP for all OSPF-learned routes
- Transport-address set to router loopback

### IPsec (Stub Configuration)
- VTI tunnel between PE1-BLR and PE1-DEL (172.16.0.0/30)
- Configured in FRR as interface tunnel1 with static IP
- IKEv2 with ESP encryption (config stub — requires strongSwan for full operation)

---

## Deployment Commands

```bash
# Deploy topology
sudo containerlab deploy --topo topology.clab.yml

# Start FRR daemons on all 10 router containers
bash scripts/start-frr.sh

# Verify all nodes running
sudo containerlab inspect --name ps13
docker ps --filter name=clab-ps13
```

---

## Verification Results

### 1. Container Status — All 11 containers running

| Container | Image | Status |
|-----------|-------|--------|
| clab-ps13-ce1-blr | frrouting/frr | up |
| clab-ps13-pe1-blr | frrouting/frr | up |
| clab-ps13-p1 | frrouting/frr | up |
| clab-ps13-ce1-mum | frrouting/frr | up |
| clab-ps13-pe1-mum | frrouting/frr | up |
| clab-ps13-p2 | frrouting/frr | up |
| clab-ps13-ce1-che | frrouting/frr | up |
| clab-ps13-pe1-che | frrouting/frr | up |
| clab-ps13-ce1-del | frrouting/frr | up |
| clab-ps13-pe1-del | frrouting/frr | up |
| clab-ps13-trex | trexcisco/trex | up |

### 2. FRR Daemons — zebra, bgpd, ospfd, ldpd running on all 10 routers

### 3. BGP Convergence — All sessions established
- **PE iBGP full mesh** (4 PEs, peer-group via loopbacks): all 6 sessions UP
- **P iBGP** (P1 ↔ P2): session UP
- **eBGP PE↔CE** (4 sessions, one per site): all UP

### 4. OSPF — All core adjacencies formed, LSDB synchronized

### 5. LDP — All label bindings exchanged across core interfaces

### 6. MPLS Forwarding — Label-switched paths operational

### 7. E2E Ping — CE loopback reachability (via MPLS LSP)

| Source | Destination | RTT | TTL | Status |
|--------|-------------|-----|-----|--------|
| CE1-BLR (3.3.3.1) | CE1-MUM (3.3.3.2) | 0.104 ms | 60 | ✅ |
| CE1-BLR (3.3.3.1) | CE1-CHE (3.3.3.3) | 0.089 ms | 61 | ✅ |
| CE1-BLR (3.3.3.1) | CE1-DEL (3.3.3.4) | 0.094 ms | 61 | ✅ |

**Command used:** `docker exec clab-ps13-ce1-blr ping -I 3.3.3.1 3.3.3.2`

---

## Key Issue Found & Fixed

### Problem: `ping 3.3.3.2` from CE1-BLR failed (100% loss)

**Root Cause:** The kernel selected the management interface IP (172.20.0.10) as the source address for ICMP echo requests. While the forward path to CE1-MUM (3.3.3.2) worked via MPLS, the **return path broke** because:

- CE routers only exchange **/32 loopback routes** via eBGP
- Backbone transit prefixes (10.0.0.0/8) are **not advertised to CEs**
- ICMP reply from CE1-MUM was sourced to 172.20.0.10 (management), which CE1-MUM has no route for
- Management network (172.20.0.0/24) is on a separate bridge, not part of the FRR routing table

**Fix:** Use explicit source address with `ping -I <loopback>`:

```bash
ping -I 3.3.3.1 3.3.3.2   # CE1-BLR → CE1-MUM ✅
ping -I 3.3.3.1 3.3.3.3   # CE1-BLR → CE1-CHE ✅
ping -I 3.3.3.1 3.3.3.4   # CE1-BLR → CE1-DEL ✅
```

**Design Implication:** This is correct behavior — CEs are MPLS-unaware and only know about their own /32 loopback prefixes. All inter-site traffic traverses the MPLS backbone transparently.

---

## Fault Injection — 7 Automation Scripts

All scripts located in `scripts/` directory:

| # | Script | Scenario | Revert? |
|---|--------|----------|---------|
| 1 | `fault-link-fail.sh` | Take P1-eth1 (P1↔P2) link down/up | Yes |
| 2 | `fault-bgp-flap.sh` | Reset BGP session between PE1-BLR ↔ PE1-MUM | Yes |
| 3 | `fault-congestion.sh` | Add 200ms + 50Mbit netem delay/loss to P1-P2 link | Yes |
| 4 | `fault-route-leak.sh` | Inject bogus prefix into BGP to simulate route leak | Yes |
| 5 | `fault-crc-errors.sh` | Add 1% packet corruption on P1-eth1 (simulates CRC) | Yes |
| 6 | `fault-node-crash.sh` | Kill all FRR daemons on P1 (simulates router crash) | Yes |
| 7 | `fault-lsp-break.sh` | Disable LDP on P1-eth1 → MPLS label path disruption | Yes |

All scripts support the `revert` argument to restore normal operation.

---

## Project Structure (After Phase 1)

```
ISRO2026/
├── topology.clab.yml           # Containerlab topology definition
├── configs/                    # FRR configs (10 routers + daemons)
│   ├── ce1-blr.cfg ... pe1-del.cfg
│   └── daemons
├── scripts/                    # Operational + fault injection scripts
│   ├── start-frr.sh            # Start FRR daemons
│   ├── fault-link-fail.sh      # (7 fault scenarios)
│   ├── fault-bgp-flap.sh
│   ├── fault-congestion.sh
│   ├── fault-route-leak.sh
│   ├── fault-crc-errors.sh
│   ├── fault-node-crash.sh
│   └── fault-lsp-break.sh
├── clab-ps13/                  # Auto-generated by Containerlab
└── Docs/phases/
    └── phase-01-network-simulation.md  # This file
```

---

## Key Files

| File | Purpose |
|------|---------|
| `topology.clab.yml` | Containerlab topology — 11 nodes, 12 links |
| `configs/daemons` | FRR daemons enabled: zebra, bgpd, ospfd, ldpd |
| `configs/*.cfg` | Per-router FRR configuration (10 files) |
| `scripts/start-frr.sh` | Batch FRR daemon startup across all containers |
| `scripts/fault-*.sh` | 7 fault injection + revert scripts |

---

## Learnings & Design Decisions

1. **Source address selection matters in MPLS networks** — Always use `ping -I <loopback>` for CE-to-CE reachability tests.
2. **CE routers are MPLS-unaware** — MPLS only exists on P and PE interfaces. CE-facing PE interfaces do NOT enable MPLS.
3. **OSPF on core only** — PEs run OSPF on backbone-facing interfaces; CE-PE links use eBGP only.
4. **Full mesh iBGP between PEs** — No route reflector needed for 4 nodes (6 sessions).
5. **P routers have minimal config** — OSPF + LDP + iBGP to other P. No VPNv4, no CE routes.
6. **Container labels matter** — Must use `clab-ps13-<name>` prefix when exec'ing into containers.
7. **IPsec is a stub** — VTI tunnel interfaces exist in config but require strongSwan for actual encryption.

---

## Next Phase

→ **Phase 2: Telemetry Pipeline** — Telegraf agents on each container → Prometheus → Kafka streaming → ELK stack
