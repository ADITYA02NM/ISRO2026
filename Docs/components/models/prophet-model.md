---
created: 2026-06-23
tags: [ps13, ml, prophet, trend, forecast]
---

# Prophet (statsmodels) — Trend Decomposition

**File**: `ml/models/prophet_model.py` | **Checkpoint**: `checkpoints/prophet.pkl` (0.3 KB) | **Engine**: statsmodels native + ONNX (verified)

## Metrics

- **Anomalies**: 15 detected via decomposition residuals
- **Forecast**: 24-hour horizon with confidence intervals
- **Model size**: 0.3 KB (metadata only — decomposition is algorithmic)

## How It Works

Uses StatsModels' seasonal decomposition (not Meta's Prophet) to decompose telemetry into:
- **Trend component**: Long-term baseline drift
- **Seasonal component**: Daily/hourly cycles
- **Residual component**: Anomalies

## Related

- [[ensemble-predictor]] — Loads via ONNX
- [[lstm-model]] — Complementary deep-learning forecast
