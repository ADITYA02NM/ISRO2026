#!/bin/bash
# setup.sh — Deploy the PS13 Telemetry Stack
# Run this AFTER the Containerlab topology is deployed and FRR daemons started.
#
# Usage:
#   ./telemetry/setup.sh          # Deploy full stack
#   ./telemetry/setup.sh down     # Tear down stack
#   ./telemetry/setup.sh status   # Check stack status

set -e

COMPOSE_FILE="telemetry/docker-compose.yml"
ACTION="${1:-up}"

case "$ACTION" in
  up)
    echo "═══ Deploying PS13 Telemetry Stack ═══"

    # Verify Containerlab is running
    if ! sudo containerlab inspect --name ps13 &>/dev/null; then
      echo "ERROR: ps13 topology is not running. Deploy first:"
      echo "  sudo containerlab deploy --topo topology.clab.yml"
      echo "  bash scripts/start-frr.sh"
      exit 1
    fi

    echo "  Starting telemetry stack..."
    docker compose -f "$COMPOSE_FILE" up -d

    echo ""
    echo "  Waiting for services to be ready..."
    sleep 10

    # Verify services
    echo ""
    echo "═══ Service Status ═══"
    docker compose -f "$COMPOSE_FILE" ps

    echo ""
    echo "═══ Endpoints ═══"
    echo "  Prometheus:  http://localhost:9090"
    echo "  Kibana:      http://localhost:5601"
    echo "  Elasticsearch: http://localhost:9200"
    echo "  Kafka UI:    http://localhost:8080  (debug profile)"
    echo ""

    # Create Kafka topics
    echo "═══ Creating Kafka topics ═══"
    bash telemetry/kafka/topic-definitions.sh

    echo ""
    echo "✅ Telemetry stack deployed."
    echo "  Telegraf collecting from all 10 FRR containers every 10s."
    echo "  Prometheus scraping Telegraf every 15s."
    echo "  Data flowing through Kafka topic: ps13-telemetry"
    echo "  Logs shipped via Filebeat → Elasticsearch"
    ;;

  down)
    echo "═══ Tearing down PS13 Telemetry Stack ═══"
    docker compose -f "$COMPOSE_FILE" down -v
    echo "✅ Telemetry stack stopped."
    ;;

  status)
    echo "═══ Telemetry Stack Status ═══"
    docker compose -f "$COMPOSE_FILE" ps
    ;;

  restart)
    echo "═══ Restarting PS13 Telemetry Stack ═══"
    docker compose -f "$COMPOSE_FILE" restart
    echo "✅ Telemetry stack restarted."
    ;;

  *)
    echo "Usage: $0 [up|down|status|restart]"
    exit 1
    ;;
esac
