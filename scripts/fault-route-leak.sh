#!/bin/bash
# fault-route-leak.sh — Scenario 4: Route Leak
# Injects a bogus prefix into BGP on PE1-CHE to simulate a route leak
# where a CE prefix leaks into the global routing table
# Usage: ./fault-route-leak.sh [revert]

set -e

NODE="clab-ps13-pe1-che"
BOGUS_PREFIX="198.51.100.0/24"
BOGUS_NEXTHOP="10.0.2.1"

if [ "$1" == "revert" ]; then
  echo "═══ Removing leaked route from $NODE ═══"
  docker exec "$NODE" vtysh -c "conf t" \
    -c "no ip route $BOGUS_PREFIX Null0" \
    -c "router bgp 65001" \
    -c "no network $BOGUS_PREFIX"
  echo "  ✓ Leaked route withdrawn. BGP will reconverge."
  echo "  Verify: docker exec $NODE vtysh -c 'show bgp' | grep $BOGUS_PREFIX"
  exit 0
fi

echo "═══ Injecting fault: Route leak from PE1-CHE ═══"
echo "  Leaking $BOGUS_PREFIX into iBGP..."

# Create a static route for the bogus prefix, then advertise it via BGP
docker exec "$NODE" vtysh -c "conf t" \
  -c "ip route $BOGUS_PREFIX Null0" \
  -c "router bgp 65001" \
  -c "network $BOGUS_PREFIX"

echo "  ✓ Route $BOGUS_PREFIX injected into BGP table."
echo "  All PEs will now have a route to this bogus network."
echo "  This simulates a CE redistributing its LAN into BGP incorrectly."
echo "  Revert with: ./fault-route-leak.sh revert"
echo "  Verify: docker exec clab-ps13-pe1-blr vtysh -c 'show bgp' | grep $BOGUS_PREFIX"
