#!/bin/bash
# start-frr.sh — Start FRR daemons in all router containers
# Run this after `sudo containerlab deploy --topo topology.clab.yml`
#
# The FRR Docker image ships with FRR installed but Containerlab's
# kind:linux keeps the container running with `sleep infinity`.
# This script execs into each container and starts FRR daemons.

set -e

NODES=(
  "ce1-blr"
  "pe1-blr"
  "p1"
  "ce1-mum"
  "pe1-mum"
  "p2"
  "ce1-che"
  "pe1-che"
  "ce1-del"
  "pe1-del"
)

start_frr() {
  local NODE=$1
  echo "═══ Starting FRR on $NODE ═══"

  # Check if zebra is already running
  if docker exec "clab-ps13-$NODE" pidof zebra &>/dev/null; then
    echo "  FRR already running on $NODE, skipping"
    return 0
  fi

  # Start FRR using the image's docker-start script
  docker exec -d "clab-ps13-$NODE" /usr/lib/frr/docker-start 2>/dev/null || {
    # Fallback: start daemons individually
    echo "  docker-start failed, starting daemons individually..."
    docker exec -d "clab-ps13-$NODE" /usr/lib/frr/zebra -f /etc/frr/frr.conf -d
    docker exec -d "clab-ps13-$NODE" /usr/lib/frr/bgpd -f /etc/frr/frr.conf -d
    docker exec -d "clab-ps13-$NODE" /usr/lib/frr/ospfd -f /etc/frr/frr.conf -d
    docker exec -d "clab-ps13-$NODE" /usr/lib/frr/ldpd -f /etc/frr/frr.conf -d
  }

  echo "  ✓ FRR started on $NODE"
}

# Verify containerlab is running
if ! sudo containerlab inspect --name ps13 &>/dev/null; then
  echo "ERROR: ps13 topology is not running. Deploy first with:"
  echo "  sudo containerlab deploy --topo topology.clab.yml"
  exit 1
fi

# Start FRR on all nodes in parallel
for NODE in "${NODES[@]}"; do
  start_frr "$NODE" &
done

wait
echo ""
echo "═══ All FRR daemons started ═══"
echo "Verify with:"
echo "  docker exec clab-ps13-ce1-blr vtysh -c 'show ip route'"
