#!/bin/bash
# fault-congestion.sh — Scenario 3: Interface Congestion
# Adds simulated delay and packet loss on P1-P2 link using netem
# Usage: ./fault-congestion.sh [revert] [delay_ms] [loss_pct]

set -e

NODE="clab-ps13-p1"
IFACE="eth1"
DELAY="${2:-200}"    # Default: 200ms latency
LOSS="${3:-10}"      # Default: 10% packet loss

if [ "$1" == "revert" ]; then
  echo "═══ Removing congestion simulation from $NODE:$IFACE ═══"
  docker exec "$NODE" tc qdisc del dev "$IFACE" root 2>/dev/null || true
  echo "  ✓ Netem qdisc removed. Normal latency restored."
  echo "  Verify: docker exec $NODE tc qdisc show dev $IFACE"
  exit 0
fi

echo "═══ Injecting fault: Interface congestion on $NODE:$IFACE ═══"
echo "  Delay: ${DELAY}ms | Loss: ${LOSS}%"

# Remove any existing qdisc first
docker exec "$NODE" tc qdisc del dev "$IFACE" root 2>/dev/null || true

# Add netem: delay + loss simulates severe congestion
docker exec "$NODE" tc qdisc add dev "$IFACE" root netem delay "${DELAY}ms" loss "${LOSS}%"

echo "  ✓ Congestion applied."
echo "  E2E traffic will experience ${DELAY}ms latency + ${LOSS}% loss."
echo "  Revert with: ./fault-congestion.sh revert"
echo "  Verify: docker exec $NODE tc qdisc show dev $IFACE"
