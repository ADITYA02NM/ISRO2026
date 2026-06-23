---
created: 2026-06-23
tags: [ps13, ml, anomaly, isolation-forest]
---

# Isolation Forest — Anomaly Detection

**File**: `ml/models/isolation_forest_model.py` | **Checkpoint**: `checkpoints/isolation_forest.pkl` | **Engine**: native (ONNX failed)

## Metrics

- **Anomaly rate**: 396 / 7,920 (5.0%)
- **Model size**: 2,108 KB (pickle)

## Purpose

Unsupervised anomaly detection on telemetry. Flags any row where metric patterns deviate from normal operation — complementary to XGBoost's supervised classification.

## Related

- [[ensemble-predictor]] — Loads this model
- [[telemetry-schema]] — Feature space
