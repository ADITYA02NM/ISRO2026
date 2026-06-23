---
created: 2026-06-23
tags: [ps13, ml, xgboost, classification]
---

# XGBoost — Fault Classification

**File**: `ml/models/xgboost_model.py` | **Checkpoint**: `checkpoints/xgboost.json` | **Engine**: native (ONNX failed)

## Metrics

- **Accuracy**: 99.94% (8-class fault classification)
- **Model size**: 1,061 KB (JSON)

## Classes

0. None (normal)
1. BGP Flap
2. Congestion
3. CRC Errors
4. Link Failure
5. LSP Break
6. Node Crash
7. Route Leak

## Related

- [[ensemble-predictor]] — Loads this model
- [[fault-scenarios]] — The 7 fault types
