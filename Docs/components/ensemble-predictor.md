---
created: 2026-06-23
tags: [ps13, ml, ensemble, core]
---

# Ensemble Predictor — `ml/ensemble_predictor.py`

**≈1400 lines.** The central inference engine that loads and runs all 7 ML models.

## Architecture

```
PredictRequest (TelemetrySnapshot)
  ↓
ensemble_predictor.py
  ├── _engineer_features()    → 109-dim feature vector (12 core + lags + stats + site means + cycle)
  ├── _engineer_fault()       → XGBoost: 8-class fault classification
  ├── _engineer_anomaly()     → IsolationForest: anomaly score (5%)
  ├── _engineer_series()      → LSTM/Autoencoder/Prophet: time-series windows
  ├── _engineer_tti()         → TTI Regressor: time-to-incident + severity + fault prob
  └── _engineer_graph()       → GNN: per-node anomaly scores (graph topology)
  ↓
PredictResult { fault, anomaly, tti, forecast, graph, meta }
```

## Model Loading

| Model | Method | Engine | File |
|-------|--------|--------|------|
| `xgboost` | `_import_model("xgboost")` | native | `checkpoints/xgboost.json` |
| `isolation_forest` | `_import_model("isolation_forest")` | native | `checkpoints/isolation_forest.pkl` |
| `autoencoder` | `_import_model("autoencoder")` | ONNX → torch fallback | `onnx/autoencoder.onnx` |
| `lstm` | `_import_model("lstm")` | torch | `checkpoints/lstm.pt` |
| `gnn` | `_import_model("gnn")` | torch | `checkpoints/gnn.pt` |
| `prophet` | `_import_model("prophet")` | statsmodels | `onnx/prophet.onnx` |
| `tti_regressor` | `_import_model("tti_regressor")` | ONNX | `onnx/tti_regressor.onnx` |

Loading sequence tries ONNX → torch → native pickle for each model.

## Feature Engineering

The [[../data/telemetry-schema|TelemetrySnapshot]] has 16 fields: 12 core features + 4 context fields.

`predict()` expands to 109 features using:
- **Lags**: `{feature}_lag_{1,2,3,6,12}h` → 60 features
- **Rolling stats**: `{feature}_rolling_mean_{3,6,12}h`, `_rolling_std_{3,6,12}h` → 24 features
- **Site means**: `{feature}_site_mean` → 12 features
- **Cycle**: `hour_sin`, `hour_cos` → 2 features
- **Passthrough**: 12 core features + 4 context fields

If feature engineering imports fail, inline fallback fills zeros (degraded but functional).

## Performance

- All 7 models load in <5 seconds
- Single prediction: ~50ms (no LLM) / ~1-3s (with LLM)
- [[air-gap-validation|Air-gap validation]]: 8/8 checks pass (all models load without network)

## Related

- [[xgboost-model]] — Fault classification (99.94%)
- [[no-index|isolation-forest-model]] — Anomaly detection
- [[no-index|autoencoder-model]] — Reconstruction anomaly
- [[no-index|lstm-model]] — Time-series forecast
- [[no-index|gnn-model]] — Graph anomaly scores
- [[no-index|prophet-model]] — Trend decomposition
- [[no-index|tti-regressor-model]] — Time-to-incident
- [[noc-copilot]] — FastAPI server that uses this
