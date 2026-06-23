---
created: 2026-06-23
tags: [ps13, ml, autoencoder, anomaly]
---

# Autoencoder — Reconstruction Anomaly

**File**: `ml/models/autoencoder_model.py` | **Checkpoint**: `checkpoints/autoencoder.pt` | **Engine**: ONNX (verified, 2.2 KB)

## Metrics

- **Training**: 73 epochs (early stopping)
- **Anomalies**: 381 / 7,920 (5.0%)
- **Threshold**: MSE reconstruction error > 5.0%
- **Model size**: 10.8 KB (.pt), 2.2 KB (ONNX)

## How It Works

Learns normal network behavior patterns. When a telemetry sample is fed through the encoder-decoder, a high reconstruction error indicates anomalous behavior unseen during training.

## Related

- [[ensemble-predictor]] — Loads via ONNX
- [[isolation-forest-model]] — Complementary anomaly detector
