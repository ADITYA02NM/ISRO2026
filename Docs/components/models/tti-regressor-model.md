---
created: 2026-06-23
tags: [ps13, ml, tti, regression]
---

# TTI Regressor — Time-to-Incident

**File**: `ml/models/tti_regressor_model.py` | **Checkpoint**: `checkpoints/tti_regressor.pkl` | **Engine**: ONNX (verified)

## Note: File Naming

The file is `tti_regressor_model.py` (not `tti_regressor.py`). This matters because `ensemble_predictor.py` imported `models.tti_regressor` — fixed to `models.tti_regressor_model`.

## Metrics

| Target | Metric | Value |
|--------|--------|-------|
| TTI (hours) | MAE | 10.04h |
| Severity | R² | 0.98 |
| Fault Probability | R² | 0.95 |

## 3-Target Output

1. **Time-to-Incident** (hours) — How long until network impact
2. **Severity** (0-1) — Predicted severity score
3. **Fault Probability** (0-1) — Likelihood of actual fault

## Related

- [[ensemble-predictor]] — Loads via ONNX
- [[prophet-model]] — Complementary forecast model
