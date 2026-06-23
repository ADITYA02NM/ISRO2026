#!/bin/bash
# fault-bgp-flap.sh — Scenario 2: BGP Session Flap
# Resets the iBGP session between PE1-BLR and PE1-MUM
# Usage: ./fault-bgp-flap.sh [revert]

set -e

PEER_A="clab-ps13-pe1-blr"
PEER_B="clab-ps13-pe1-mum"
REMOTE_AS="65001"

if [ "$1" == "revert" ]; then
  echo "═══ No explicit revert needed — BGP auto-recovers after flap ═══"
  echo "  iBGP session will automatically re-establish after reset."
  echo "  Verify:"
  echo "    docker exec $PEER_A vtysh -c 'show bgp summary'"
  echo "    docker exec $PEER_B vtysh -c 'show bgp summary'"
  exit 0
fi

echo "═══ Injecting fault: BGP session flap PE1-BLR ↔ PE1-MUM ═══"

echo "  Clearing BGP session on PE1-BLR → PE1-MUM..."
docker exec "$PEER_A" vtysh -c "clear bgp $REMOTE_AS 2.2.2.2"

echo "  ✓ BGP session reset. Session will re-establish immediately."
echo "  Routes may temporarily withdraw and re-advertise."
echo "  Monitor with: docker exec $PEER_A vtysh -c 'show bgp summary'"
