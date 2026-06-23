#!/bin/bash
# fault-node-crash.sh — Scenario 6: Node Crash
# Kills FRR daemons on P1 to simulate a router crash/reboot
# Usage: ./fault-node-crash.sh [revert]

set -e

NODE="clab-ps13-p1"

if [ "$1" == "revert" ]; then
  echo "═══ Restoring FRR on $NODE (restarting daemons) ═══"
  docker exec -d "$NODE" /usr/lib/frr/docker-start 2>/dev/null || {
    docker exec -d "$NODE" /usr/lib/frr/zebra -f /etc/frr/frr.conf -d
    sleep 1
    docker exec -d "$NODE" /usr/lib/frr/bgpd -f /etc/frr/frr.conf -d
    docker exec -d "$NODE" /usr/lib/frr/ospfd -f /etc/frr/frr.conf -d
    docker exec -d "$NODE" /usr/lib/frr/ldpd -f /etc/frr/frr.conf -d
  }
  echo "  ✓ FRR daemons restarted on $NODE."
  echo "  OSPF + BGP + LDP will reconverge in ~30-60s."
  echo "  Verify: docker exec $NODE vtysh -c 'show ip route'"
  exit 0
fi

echo "═══ Injecting fault: Router crash on $NODE ═══"
echo "  Killing all FRR daemons (zebra, bgpd, ospfd, ldpd)..."

docker exec "$NODE" pkill -9 zebra 2>/dev/null || true
docker exec "$NODE" pkill -9 bgpd 2>/dev/null || true
docker exec "$NODE" pkill -9 ospfd 2>/dev/null || true
docker exec "$NODE" pkill -9 ldpd 2>/dev/null || true

echo "  ✓ All FRR daemons killed on $NODE."
echo "  P1 is effectively crashed — no routing, no MPLS forwarding."
echo "  Traffic will reroute via alternate paths if available."
echo "  Revert with: ./fault-node-crash.sh revert"
echo "  Verify: docker exec $NODE vtysh -c 'show ip route'  (will show error)"
