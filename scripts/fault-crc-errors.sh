#!/bin/bash
# fault-crc-errors.sh — Scenario 5: CRC Errors on Interface
# Adds packet corruption on P1-eth1 to simulate interface CRC/bit errors
# Usage: ./fault-crc-errors.sh [revert] [corrupt_pct]

set -e

NODE="clab-ps13-p1"
IFACE="eth1"
CORRUPT="${2:-1}"    # Default: 1% packet corruption

if [ "$1" == "revert" ]; then
  echo "═══ Removing CRC error simulation from $NODE:$IFACE ═══"
  docker exec "$NODE" tc qdisc del dev "$IFACE" root 2>/dev/null || true
  echo "  ✓ Netem corrupt qdisc removed."
  echo "  Verify: docker exec $NODE tc qdisc show dev $IFACE"
  exit 0
fi

echo "═══ Injecting fault: CRC errors on $NODE:$IFACE ═══"
echo "  Corruption: ${CORRUPT}% of packets"

# Remove any existing qdisc first
docker exec "$NODE" tc qdisc del dev "$IFACE" root 2>/dev/null || true

# Add netem corrupt — simulates bit errors / CRC failures at layer 1
docker exec "$NODE" tc qdisc add dev "$IFACE" root netem corrupt "${CORRUPT}%"

echo "  ✓ ${CORRUPT}% packet corruption applied to $IFACE."
echo "  Upper-layer protocols (TCP retransmits, OSPF LSResync) will react."
echo "  Revert with: ./fault-crc-errors.sh revert"
echo "  Verify: docker exec $NODE tc qdisc show dev $IFACE"
