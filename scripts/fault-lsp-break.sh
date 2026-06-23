#!/bin/bash
# fault-lsp-break.sh — Scenario 7: MPLS LSP Break
# Disables LDP on P1-eth1 (P1-P2 link) to break MPLS label path
# OSPF still sees link as up, but MPLS forwarding breaks
# Usage: ./fault-lsp-break.sh [revert]

set -e

NODE="clab-ps13-p1"

if [ "$1" == "revert" ]; then
  echo "═══ Restoring LDP on $NODE ═══"
  docker exec "$NODE" vtysh -c "conf t" \
    -c "mpls ldp" \
    -c "address-family ipv4" \
    -c "interface eth1" \
    -c "exit" \
    -c "exit" \
    -c "exit"
  echo "  ✓ LDP re-enabled on $NODE-eth1."
  echo "  LDP neighbors will reconverge and labels redistribute."
  echo "  Verify: docker exec $NODE vtysh -c 'show mpls ldp neighbor'"
  exit 0
fi

echo "═══ Injecting fault: MPLS LSP break on $NODE-eth1 ═══"
echo "  Disabling LDP on P1-eth1 while leaving OSPF up..."

docker exec "$NODE" vtysh -c "conf t" \
  -c "mpls ldp" \
  -c "address-family ipv4" \
  -c "no interface eth1" \
  -c "exit" \
  -c "exit" \
  -c "exit"

echo "  ✓ LDP disabled on P1-eth1."
echo "  OSPF adjacency still up — link appears healthy."
echo "  But MPLS labels not exchanged — LSP broken."
echo "  Effect: MPLS traffic blackholes despite OSPF convergence."
echo "  Revert with: ./fault-lsp-break.sh revert"
echo "  Verify: docker exec $NODE vtysh -c 'show mpls ldp neighbor'"
