---
created: 2026-06-23
tags: [ps13, architecture, ml]
---

# ML Pipeline Architecture

## Data Flow

```
TelemetrySnapshot (16 fields)
         │
         ▼
  ┌─────────────────────────────┐
  │   Feature Engineering        │
  │  - 12 core features          │
  │  - Rolling windows (1/3/6/12h)│
  │  - Site/role aggregates      │
  │  - Ratios & cyclic encoding  │
  │  - Delta from site mean      │
  │  → 109 total features        │
  └─────────────┬───────────────┘
                │
                ▼
  ┌─────────────────────────────┐
  │   Ensemble Predictor         │
  │                              │
  │  ┌─────────┐ ┌────────────┐  │
  │  │ XGBoost │ │Isolation   │  │
  │  │(fault)  │ │Forest(anom)│  │
  │  └────┬────┘ └─────┬──────┘  │
  │  ┌─────────┐ ┌────────────┐  │
  │  │TTI Reg  │ │Prophet     │  │
  │  │(3-target)│ │(forecast)  │  │
  │  └────┬────┘ └─────┬──────┘  │
  │  ┌─────────┐ ┌────────────┐  │
  │  │Autoenc  │ │LSTM        │  │
  │  │(recon)  │ │(seq pred)  │  │
  │  └────┬────┘ └─────┬──────┘  │
  │  ┌─────────┐                 │
  │  │  GNN    │                 │
  │  │(graph)  │                 │
  │  └────┬────┘                 │
  └───────┼─────────────────────┘
          │
          ▼
  ┌─────────────────────────────┐
  │  DiagnosisResult (JSON)     │
  │  - Fault: type + confidence │
  │  - Anomaly: score + flag    │
  │  - TTI: hours + severity    │
  │  - Forecast: 24h trend      │
  │  - AE: reconstruction error │
  │  - LSTM: 12h prediction     │
  │  - GNN: node anomaly scores │
  └─────────────┬───────────────┘
                │
        ┌───────┴───────┐
        ▼               ▼
  ┌──────────┐   ┌──────────────┐
  │ LLM/     │   │ Dashboard    │
  │ Explain  │   │ (Three.js)   │
  │ (Ollama) │   │              │
  └──────────┘   └──────────────┘
```

## Model Loading Strategy

```python
def load_model_with_fallback(name, paths):
    """
    1. Try ONNX Runtime (fastest inference)
    2. Fall back to PyTorch (torch.jit / torch.load)
    3. Fall back to native (pickle, json)
    """
```

| Model | Primary | Fallback 1 | Fallback 2 |
|-------|---------|------------|------------|
| XGBoost | onnx | — | native json |
| IsolationForest | onnx | — | native pkl |
| TTI Regressor | onnx | pkl | — |
| Prophet | onnx | — | statsmodels |
| Autoencoder | onnx | torch.pt | — |
| LSTM | torch.pt | — | — |
| GNN | torch.pt | — | — |

## Feature Engineering (`ensemble_predictor.py`)

```
Input: 16 fields (12 core + 4 context)
  ├── Rolling windows: mean, std, min, max, slope
  │   └── Windows: 1h, 3h, 6h, 12h → 48 features
  ├── Site aggregates: site_mean for each metric → 12 features
  ├── Role aggregates: role_mean for each metric → 12 features
  ├── Ratios: bw/utilization, mem/bw → 6 features
  ├── Delta features: Δ from site_mean → 12 features
  ├── Historical: anomaly scores from window statistics → 5 features
  └── Cyclic: hour_sin, hour_cos → 2 features
Total: 109 features
```
