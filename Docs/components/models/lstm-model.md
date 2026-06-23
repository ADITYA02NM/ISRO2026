---
created: 2026-06-23
tags: [ps13, ml, lstm, timeseries]
---

# LSTM — Time-Series Forecasting

**File**: `ml/models/lstm_model.py` | **Checkpoint**: `checkpoints/lstm.pt` | **Engine**: torch (ONNX export failed)

## Metrics

- **Training**: 100 epochs
- **Val loss**: 271.37
- **Model size**: 482.5 KB

## ONNX Export Failure

`torch.export` fails with shape conflict on `seq_length=12` static dim. This is a PyTorch 2.12+ `torch.export` limitation with dynamic axes. Falls back to PyTorch (.pt) runtime.

## Purpose

Predicts time-series metrics (latency, jitter, throughput) 12 steps ahead as a sequence-to-sequence model.

## Related

- [[ensemble-predictor]] — Loads via torch
- [[prophet-model]] — Complementary statistical forecast
