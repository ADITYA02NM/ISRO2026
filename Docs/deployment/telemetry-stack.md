---
created: 2026-06-23
tags: [ps13, deployment, telemetry, docker]
---

# Telemetry Pipeline — Docker Stack

**Not deployed** (configs ready). Docker Compose stack at `telemetry/docker-compose.yml`.

## Architecture (T1 / T2 / T3)

```
T1: Telegraf ──▶ Kafka ──▶ Filebeat ──▶ Elasticsearch ──▶ Kibana
                    │
                    └────────▶ WebSocket ──▶ (Future dashboards)
                       
T2: Prometheus ──▶ AlertManager ──▶ (Webhook to NOC Copilot)

T3: Database + Historical analytics
```

## Components

| Service | Config | Port | Purpose |
|---------|--------|------|---------|
| Telegraf | `telemetry/telegraf/telegraf.conf` | — | Metrics collector (agent on each device) |
| Kafka | `telemetry/kafka/topic-definitions.sh` | 9092 | Stream buffer |
| Prometheus | `telemetry/prometheus/prometheus.yml` | 9090 | Time-series DB |
| AlertManager | `telemetry/prometheus/alert_rules.yml` | 9093 | Alert routing |
| Elasticsearch | `telemetry/elasticsearch/elasticsearch.yml` | 9200 | Log storage |
| Kibana | `telemetry/kibana/kibana.yml` | 5601 | Visualization |
| Filebeat | `telemetry/filebeat/filebeat.yml` | — | Log shipper |

## Start

```bash
cd /home/ego/Documents/ISRO2026
docker compose -f telemetry/docker-compose.yml up -d
```

## Related

- [[telemetry-schema]] — The data flowing through this pipeline
- [[server-startup]] — How the Copilot server connects
