#!/bin/bash
# fault-link-fail.sh — Scenario 1: Link Failure
# Takes down / brings up the P1-P2 core link (eth1 on both routers)
# Usage: ./fault-link-fail.sh [revert]

set -e

NODE_A="clab-ps13-p1"
NODE_B="clab-ps13-p2"
IFACE="eth1"

if [ "$1" == "revert" ]; then
  echo "═══ Restoring P1-P2 link (bringing iface up) ═══"
  docker exec "$NODE_A" ip link set "$IFACE" up
  docker exec "$NODE_B" ip link set "$IFACE" up
  echo "  ✓ Link restored. OSPF + LDP will reconverge in ~30s."
  echo "  Verify: docker exec $NODE_A vtysh -c 'show ip ospf neighbor'"
else
  echo "═══ Injecting fault: P1-P2 link DOWN ═══"
  docker exec "$NODE_A" ip link set "$IFACE" down
  docker exec "$NODE_B" ip link set "$IFACE" down
  echo "  ✓ Link down on both P1-eth1 and P2-eth1."
  echo "  OSPF will detect failure in ~40s (dead interval)."
  echo "  Traffic will reroute via P1→PE1-CHE→P2 if alternate path exists."
  echo "  Revert with: ./fault-link-fail.sh revert"
fi
