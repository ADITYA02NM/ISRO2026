---
created: 2026-06-23
tags: [ps13, ml, gnn, graph]
---

# GNN — Graph Anomaly Scores

**File**: `ml/models/gnn_model.py` | **Checkpoint**: `checkpoints/gnn.pt` (3.4 KB) | **Engine**: torch (ONNX export failed)

## Architecture

GCNEncoder with 10-node graph (11 devices minus 1). Each node represents a network device, edges represent MPLS connections between sites.

## Training

- **Epochs**: 100
- **Final loss**: 0.249
- **Model size**: 3.4 KB

## ONNX Export Failure

`AssertionError '1 not in VR[10,10]'` on GCNEncoder. Static shape issue with PyTorch 2.12+ `torch.export`.

## Purpose

Per-node anomaly scores across the network topology. Unlike other models that work per-device, GNN considers the graph structure (which devices connect to which) to detect topology-aware anomalies.

## Related

- [[ensemble-predictor]] — Loads via torch
- [[network-topology]] — The graph structure matches this topology
