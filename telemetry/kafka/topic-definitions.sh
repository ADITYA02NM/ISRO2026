#!/bin/bash
# topic-definitions.sh — Create Kafka topics for PS13 telemetry pipeline
# Run after Kafka container is up.
# Usage: ./topic-definitions.sh

set -e

KAFKA_CONTAINER="ps13-kafka"
BOOTSTRAP_SERVER="localhost:9092"

# Wait for Kafka to be ready
echo "═══ Waiting for Kafka to be ready... ═══"
for i in $(seq 1 30); do
  if docker exec "$KAFKA_CONTAINER" kafka-topics.sh --bootstrap-server "$BOOTSTRAP_SERVER" --list &>/dev/null; then
    echo "  Kafka ready after ${i}s"
    break
  fi
  sleep 2
done

echo "═══ Creating topics ═══"

create_topic() {
  local TOPIC=$1
  local PARTITIONS=$2
  local RETENTION=$3
  echo "  Creating topic: $TOPIC (${PARTITIONS} partitions, ${RETENTION} retention)"
  docker exec "$KAFKA_CONTAINER" \
    kafka-topics.sh --create \
    --bootstrap-server "$BOOTSTRAP_SERVER" \
    --topic "$TOPIC" \
    --partitions "$PARTITIONS" \
    --replication-factor 1 \
    --config "retention.ms=$RETENTION" 2>/dev/null || \
    echo "  Topic $TOPIC already exists"
}

create_topic "ps13-telemetry"   3 604800000   # 7 days
create_topic "ps13-alerts"      2 2592000000  # 30 days
create_topic "ps13-events"      2 604800000   # 7 days
create_topic "ps13-logs"        3 2592000000  # 30 days

echo ""
echo "═══ Topics created. Listing: ═══"
docker exec "$KAFKA_CONTAINER" kafka-topics.sh --bootstrap-server "$BOOTSTRAP_SERVER" --list
