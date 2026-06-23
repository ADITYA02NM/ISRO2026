"""
Unified ensemble predictor combining all 7 models for PS13 project.

Loads trained models and their ONNX exports, runs inference, and produces
unified predictions with confidence scores.

Voting strategies:
- fault_detection: majority vote (XGBoost + IsolationForest + Autoencoder + GNN)
- time_series_forecast: weighted average (LSTM + Prophet)
- tti_estimate: RandomForestRegressor (TTI) with confidence from ensemble variance
"""

from __future__ import annotations

import json
import os
import pickle
import warnings
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# ---------------------------------------------------------------------------
# Graceful dependency imports
# ---------------------------------------------------------------------------
try:
    import torch
    import torch.nn as nn

    _HAS_TORCH = True
except ImportError:
    torch = None
    nn = None
    _HAS_TORCH = False

try:
    import onnxruntime as ort

    _HAS_ONNX_RUNTIME = True
except ImportError:
    ort = None
    _HAS_ONNX_RUNTIME = False

try:
    import xgboost as xgb

    _HAS_XGB = True
except ImportError:
    xgb = None
    _HAS_XGB = False

try:
    from sklearn.ensemble import IsolationForest, RandomForestRegressor
    from sklearn.preprocessing import LabelEncoder, StandardScaler

    _HAS_SKLEARN = True
except ImportError:
    IsolationForest = None
    RandomForestRegressor = None
    LabelEncoder = None
    StandardScaler = None
    _HAS_SKLEARN = False

try:
    from statsmodels.tsa.seasonal import seasonal_decompose as _seasonal_decompose
    from statsmodels.tsa.statespace.sarimax import SARIMAX as _SARIMAX

    _HAS_STATS = True
except ImportError:
    _seasonal_decompose = None
    _SARIMAX = None
    _HAS_STATS = False

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FAULT_CLASSES_SORTED: list[str] = [
    "bgp_flap",
    "congestion",
    "crc_errors",
    "link_fail",
    "lsp_break",
    "node_crash",
    "none",
    "route_leak",
]

FAULT_LABELS: list[str] = [
    "none",
    "link_fail",
    "bgp_flap",
    "congestion",
    "route_leak",
    "crc_errors",
    "node_crash",
    "lsp_break",
]

COMMON_FEATURES: list[str] = [
    "cpu_util_pct",
    "memory_util_pct",
    "interface_bandwidth_util_pct",
    "latency_ms",
    "packet_loss_pct",
    "jitter_ms",
    "tcp_retransmits_pct",
    "bgp_prefix_count",
    "ospf_lsa_count",
    "ldp_label_count",
    "mpls_label_stack_depth",
    "flow_count",
]

XGB_FEATURE_NAMES: list[str] = [
    "throughput_bps",
    "latency_ms",
    "jitter_ms",
    "packet_loss_pct",
    "crc_error_count",
    "bgp_update_count",
    "cpu_util_pct",
    "memory_util_pct",
]

ISOLATION_FEATURES: list[str] = [
    "cpu_util_pct",
    "memory_util_pct",
    "interface_bandwidth_util_pct",
    "latency_ms",
    "packet_loss_pct",
    "jitter_ms",
    "bgp_prefix_count",
    "ospf_lsa_count",
    "ldp_label_count",
    "tcp_retransmits_pct",
    "flow_count",
]

SITE_AGG_FEATURES: list[str] = [
    "cpu_util_pct",
    "memory_util_pct",
    "interface_bandwidth_util_pct",
    "latency_ms",
    "packet_loss_pct",
    "jitter_ms",
]

AE_FEATURES: list[str] = ISOLATION_FEATURES

LSTM_FEATURES: list[str] = ISOLATION_FEATURES

LSTM_OUTPUTS: list[str] = [
    "latency_ms",
    "packet_loss_pct",
    "cpu_util_pct",
    "interface_bandwidth_util_pct",
]

TTI_TARGETS: list[str] = [
    "time_to_incident_hours",
    "severity_score",
    "fault_probability",
]

GNN_NODE_NAMES: list[str] = [
    "PE1-BLR",
    "P1-BLR",
    "PE1-MUM",
    "P1-MUM",
    "PE1-CHE",
    "PE1-DEL",
    "P1-DEL",
    "CE1-BLR",
    "CE1-MUM",
    "CE1-CHE",
]

GNN_EDGES: list[tuple[str, str]] = [
    ("PE1-BLR", "P1-BLR"),
    ("P1-BLR", "PE1-MUM"),
    ("PE1-MUM", "P1-MUM"),
    ("P1-MUM", "PE1-CHE"),
    ("PE1-MUM", "PE1-CHE"),
    ("P1-BLR", "PE1-DEL"),
    ("PE1-DEL", "P1-DEL"),
    ("CE1-BLR", "PE1-BLR"),
    ("CE1-MUM", "PE1-MUM"),
    ("CE1-CHE", "PE1-CHE"),
    ("CE1-DEL", "PE1-DEL"),
]

GNN_FEATURE_NAMES: list[str] = [
    "latency",
    "packet_loss",
    "cpu",
    "bandwidth",
    "bgp_prefix",
    "mpls_depth",
    "tcp_retrans",
]

SEQ_LENGTH = 12
PRED_STEPS = 3

# Map XGB feature names to common telemetry columns (for inference mapping)
XGB_TO_COMMON: dict[str, str | None] = {
    "throughput_bps": "interface_bandwidth_util_pct",
    "latency_ms": "latency_ms",
    "jitter_ms": "jitter_ms",
    "packet_loss_pct": "packet_loss_pct",
    "crc_error_count": None,
    "bgp_update_count": "bgp_prefix_count",
    "cpu_util_pct": "cpu_util_pct",
    "memory_util_pct": "memory_util_pct",
}

# ---------------------------------------------------------------------------
# Minimal PyTorch architecture definitions (used when loading .pt checkpoints)
# Only defined when torch is available.
# ---------------------------------------------------------------------------


if _HAS_TORCH:

    class _AutoencoderArch(nn.Module):
        def __init__(self, n_features: int = len(AE_FEATURES)) -> None:
            super().__init__()
            self.encoder = nn.Sequential(
                nn.Linear(n_features, 32),
                nn.ReLU(),
                nn.Dropout(0.1),
                nn.Linear(32, 16),
                nn.ReLU(),
            )
            self.decoder = nn.Sequential(
                nn.Linear(16, 32),
                nn.ReLU(),
                nn.Linear(32, n_features),
                nn.Sigmoid(),
            )

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.decoder(self.encoder(x))

    class _GCNLayer(nn.Module):
        def __init__(self, in_dim: int, out_dim: int) -> None:
            super().__init__()
            self.W = nn.Parameter(torch.empty(in_dim, out_dim))
            nn.init.xavier_uniform_(self.W)

        def forward(self, X: torch.Tensor, A_hat: torch.Tensor) -> torch.Tensor:
            return A_hat @ X @ self.W

    class _GCNEncoder(nn.Module):
        def __init__(self, in_dim: int = 7, hidden_dim: int = 16, out_dim: int = 8) -> None:
            super().__init__()
            self.conv1 = _GCNLayer(in_dim, hidden_dim)
            self.relu = nn.ReLU()
            self.dropout = nn.Dropout(0.1)
            self.conv2 = _GCNLayer(hidden_dim, out_dim)

        def forward(self, X: torch.Tensor, A_hat: torch.Tensor) -> torch.Tensor:
            h = self.conv1(X, A_hat)
            h = self.relu(h)
            h = self.dropout(h)
            h = self.conv2(h, A_hat)
            return h

    class _AnomalyScorer(nn.Module):
        def __init__(self, embed_dim: int = 8) -> None:
            super().__init__()
            self.fc = nn.Linear(embed_dim, 1)
            self.sigmoid = nn.Sigmoid()

        def forward(self, Z: torch.Tensor) -> torch.Tensor:
            return self.sigmoid(self.fc(Z)).squeeze(-1)

    class _GNNArch(nn.Module):
        def __init__(self, in_dim: int = 7, hidden_dim: int = 16, embed_dim: int = 8) -> None:
            super().__init__()
            self.encoder = _GCNEncoder(in_dim, hidden_dim, embed_dim)
            self.scorer = _AnomalyScorer(embed_dim)

        def forward(
            self, X: torch.Tensor, A_hat: torch.Tensor
        ) -> tuple[torch.Tensor, torch.Tensor]:
            Z = self.encoder(X, A_hat)
            scores = self.scorer(Z)
            return Z, scores

    class _LSTMArch(nn.Module):
        def __init__(
            self,
            n_features: int = len(LSTM_FEATURES),
            n_outputs: int = len(LSTM_OUTPUTS),
            hidden_sizes: tuple[int, int] = (128, 64),
        ) -> None:
            super().__init__()
            self.lstm1 = nn.LSTM(
                input_size=n_features,
                hidden_size=hidden_sizes[0],
                num_layers=1,
                batch_first=True,
            )
            self.drop1 = nn.Dropout(0.2)
            self.lstm2 = nn.LSTM(
                input_size=hidden_sizes[0],
                hidden_size=hidden_sizes[1],
                num_layers=1,
                batch_first=True,
            )
            self.drop2 = nn.Dropout(0.2)
            self.regressor = nn.Linear(hidden_sizes[1], n_outputs * PRED_STEPS)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            out, _ = self.lstm1(x)
            out = self.drop1(out)
            out, _ = self.lstm2(out)
            out = self.drop2(out)
            out = out[:, -1, :]
            out = self.regressor(out)
            return out.view(-1, PRED_STEPS, len(LSTM_OUTPUTS))

else:

    class _AutoencoderArch:  # type: ignore
        pass

    class _GNNArch:  # type: ignore
        pass

    class _LSTMArch:  # type: ignore
        pass


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def _softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Numerically stable softmax."""
    x_max = np.max(x, axis=axis, keepdims=True)
    exp_x = np.exp(x - x_max)
    return exp_x / np.sum(exp_x, axis=axis, keepdims=True)


def _normalize_adj(A: np.ndarray) -> np.ndarray:
    """Symmetric normalized adjacency with self-loops."""
    A_aug = A + np.eye(A.shape[0], dtype=A.dtype)
    D = A_aug.sum(axis=1)
    D_inv_sqrt = np.diag(D**-0.5)
    return D_inv_sqrt @ A_aug @ D_inv_sqrt


def _build_adjacency() -> np.ndarray:
    """Build numpy adjacency matrix from edge list."""
    n = len(GNN_NODE_NAMES)
    A = np.zeros((n, n), dtype=np.float32)
    name_to_idx = {name: i for i, name in enumerate(GNN_NODE_NAMES)}
    for src, dst in GNN_EDGES:
        if src in name_to_idx and dst in name_to_idx:
            i, j = name_to_idx[src], name_to_idx[dst]
            A[i, j] = 1.0
            A[j, i] = 1.0
    return A


# ═══════════════════════════════════════════════════════════════════════════
# EnsemblePredictor
# ═══════════════════════════════════════════════════════════════════════════


class EnsemblePredictor:
    """Loads all 7 models and provides a unified prediction interface.

    Voting strategies:
    - fault_detection: majority vote (XGBoost + IsolationForest + Autoencoder + GNN)
    - time_series_forecast: weighted average (LSTM + Prophet)
    - tti_estimate: RandomForestRegressor (TTI) with confidence from ensemble variance
    """

    def __init__(
        self,
        models_dir: str | None = None,
        onnx_dir: str | None = None,
        device: str = "auto",
    ) -> None:
        _BASE = Path(__file__).resolve().parent
        self.models_dir = Path(models_dir) if models_dir else _BASE / "models"
        self.onnx_dir = Path(onnx_dir) if onnx_dir else _BASE / "models" / "onnx"
        self.checkpoints_dir = self.models_dir / "checkpoints"
        self.device = self._resolve_device(device)

        # Lazy-load cache: name -> loaded model object
        self._models: dict[str, Any] = {}

        self._warnings: list[str] = []

    # ── Device resolution ────────────────────────────────────────────────

    @staticmethod
    def _resolve_device(device: str) -> str:
        if device == "auto":
            if _HAS_TORCH and torch.cuda.is_available():
                return "cuda"
            return "cpu"
        return device

    # ── Public load interface ────────────────────────────────────────────

    def load_model(self, model_name: str) -> Any:
        """Lazy-load a model by name. Returns the model object or None."""
        if model_name in self._models:
            return self._models[model_name]

        loader = getattr(self, f"_load_{model_name}", None)
        if loader is None:
            warnings.warn(f"No loader defined for model '{model_name}'")
            self._models[model_name] = None
            return None

        try:
            model = loader()
            self._models[model_name] = model
            if model is None:
                self._warnings.append(f"model '{model_name}' could not be loaded")
            return model
        except Exception as exc:
            msg = f"Failed to load model '{model_name}': {exc}"
            warnings.warn(msg)
            self._warnings.append(msg)
            self._models[model_name] = None
            return None

    # ── Individual model loaders ─────────────────────────────────────────

    def _load_xgboost(self) -> Any:
        # 1) Try ONNX
        onnx_path = self.onnx_dir / "xgboost.onnx"
        if onnx_path.exists() and _HAS_ONNX_RUNTIME:
            try:
                session = ort.InferenceSession(str(onnx_path))
                return {"engine": "onnx", "session": session, "type": "xgboost"}
            except Exception:
                pass

        # 2) Try native XGBoost
        json_path = self.checkpoints_dir / "xgboost.json"
        if json_path.exists() and _HAS_XGB:
            try:
                model = xgb.XGBClassifier()
                model.load_model(str(json_path))
                return {"engine": "native", "model": model, "type": "xgboost"}
            except Exception:
                pass

        return None

    def _load_isolation_forest(self) -> Any:
        # 1) Try ONNX
        onnx_path = self.onnx_dir / "isolation_forest.onnx"
        if onnx_path.exists() and _HAS_ONNX_RUNTIME:
            try:
                session = ort.InferenceSession(str(onnx_path))
                return {
                    "engine": "onnx",
                    "session": session,
                    "type": "isolation_forest",
                }
            except Exception:
                pass

        # 2) Try pickle
        pkl_path = self.checkpoints_dir / "isolation_forest.pkl"
        if pkl_path.exists() and _HAS_SKLEARN:
            try:
                with open(pkl_path, "rb") as f:
                    model = pickle.load(f)
                return {"engine": "native", "model": model, "type": "isolation_forest"}
            except Exception:
                pass

        return None

    def _load_autoencoder(self) -> Any:
        # 1) Try ONNX
        onnx_path = self.onnx_dir / "autoencoder.onnx"
        if onnx_path.exists() and _HAS_ONNX_RUNTIME:
            try:
                session = ort.InferenceSession(str(onnx_path))
                return {"engine": "onnx", "session": session, "type": "autoencoder"}
            except Exception:
                pass

        # 2) Try PyTorch state_dict
        pt_path = self.checkpoints_dir / "autoencoder.pt"
        scaler_path = self.checkpoints_dir / "autoencoder_scaler.pkl"
        if pt_path.exists() and _HAS_TORCH:
            try:
                model = _AutoencoderArch()
                state = torch.load(pt_path, map_location=self.device)
                model.load_state_dict(state)
                model.to(self.device)
                model.eval()

                scaler = None
                if scaler_path.exists():
                    with open(scaler_path, "rb") as f:
                        scaler = pickle.load(f)

                return {
                    "engine": "torch",
                    "model": model,
                    "scaler": scaler,
                    "type": "autoencoder",
                }
            except Exception:
                pass

        return None

    def _load_gnn(self) -> Any:
        # 1) Try ONNX
        onnx_path = self.onnx_dir / "gnn.onnx"
        if onnx_path.exists() and _HAS_ONNX_RUNTIME:
            try:
                session = ort.InferenceSession(str(onnx_path))
                return {"engine": "onnx", "session": session, "type": "gnn"}
            except Exception:
                pass

        # 2) Try PyTorch state_dict
        pt_path = self.checkpoints_dir / "gnn.pt"
        if pt_path.exists() and _HAS_TORCH:
            try:
                model = _GNNArch()
                state = torch.load(pt_path, map_location=self.device)
                model.load_state_dict(state)
                model.to(self.device)
                model.eval()
                return {"engine": "torch", "model": model, "type": "gnn"}
            except Exception:
                pass

        return None

    def _load_lstm(self) -> Any:
        # 1) Try ONNX
        onnx_path = self.onnx_dir / "lstm.onnx"
        if onnx_path.exists() and _HAS_ONNX_RUNTIME:
            try:
                session = ort.InferenceSession(str(onnx_path))
                return {"engine": "onnx", "session": session, "type": "lstm"}
            except Exception:
                pass

        # 2) Try PyTorch state_dict
        pt_path = self.checkpoints_dir / "lstm.pt"
        if pt_path.exists() and _HAS_TORCH:
            try:
                model = _LSTMArch()
                state = torch.load(pt_path, map_location=self.device)
                model.load_state_dict(state)
                model.to(self.device)
                model.eval()
                return {"engine": "torch", "model": model, "type": "lstm"}
            except Exception:
                pass

        return None

    def _load_prophet(self) -> Any:
        if not _HAS_STATS:
            return None
        return {"engine": "statsmodels", "type": "prophet"}

    def _load_tti_regressor(self) -> Any:
        # 1) Try ONNX
        onnx_path = self.onnx_dir / "tti_regressor.onnx"
        if onnx_path.exists() and _HAS_ONNX_RUNTIME:
            try:
                session = ort.InferenceSession(str(onnx_path))
                return {"engine": "onnx", "session": session, "type": "tti"}
            except Exception:
                pass

        # 2) Try pickle (including fallback pkl)
        for candidate in [
            self.checkpoints_dir / "tti_regressor.pkl",
            self.onnx_dir / "tti_regressor.pkl",
        ]:
            if candidate.exists() and _HAS_SKLEARN:
                try:
                    with open(candidate, "rb") as f:
                        model = pickle.load(f)
                    return {"engine": "native", "model": model, "type": "tti"}
                except Exception:
                    pass

        return None

    # ── Feature engineering helpers (inference-time) ─────────────────────
    # Uses model module's own engineering when columns align; falls back to
    # simplified inline versions when they don't.

    def _engineer_xgboost(self, df_row: pd.DataFrame) -> pd.DataFrame:
        """Engineer XGBoost features, preferring the module's own logic."""
        _xgb_eng = None
        for _mod in ("models.xgboost_model", "ml.models.xgboost_model"):
            try:
                _tmp = __import__(_mod, fromlist=["engineer_features"])
                _xgb_eng = getattr(_tmp, "engineer_features", None)
                if _xgb_eng:
                    break
            except Exception:
                continue
        if _xgb_eng:
            try:
                return _xgb_eng(df_row)
            except Exception:
                pass
        numeric_cols = df_row.select_dtypes(include=[np.number]).columns.tolist()
        pieces: list[pd.DataFrame] = [df_row[numeric_cols]]
        for col in numeric_cols:
            s = df_row[col]
            eng = pd.DataFrame(
                {
                    f"{col}_lag_1": [s.iloc[-1]] if len(s) > 0 else [0],
                    f"{col}_rolling_mean_6": [s.tail(6).mean()],
                    f"{col}_rolling_std_6": [s.tail(6).std() if len(s) >= 2 else 0.0],
                    f"{col}_delta": [s.diff().iloc[-1] if len(s) >= 2 else 0.0],
                }
            )
            pieces.append(eng)
        return pd.concat(pieces, axis=1).fillna(0).astype(np.float32)

    def _engineer_isolation(self, d: pd.DataFrame) -> pd.DataFrame:
        """Engineer IsolationForest features, preferring the module's own logic."""
        _if_extract = None
        for _mod in ("models.isolation_forest_model", "ml.models.isolation_forest_model"):
            try:
                _tmp = __import__(_mod, fromlist=["extract_features"])
                _if_extract = getattr(_tmp, "extract_features", None)
                if _if_extract:
                    break
            except Exception:
                continue
        if _if_extract:
            try:
                if all(c in d.columns for c in ["cpu_util_pct", "latency_ms"]):
                    _r = _if_extract(d)
                    if _r.shape[1] == 21:
                        return _r
            except Exception:
                pass
        pieces: list[pd.DataFrame] = []
        common_cols = [c for c in ISOLATION_FEATURES if c in d.columns]
        if not common_cols:
            return pd.DataFrame()
        pieces.append(d[common_cols].fillna(0))
        # site_means — not available for single-sample inference
        for c in SITE_AGG_FEATURES:
            pieces.append(pd.DataFrame({f"site_mean_{c}": [0.0]}, index=d.index))
        for col in ("latency_ms", "packet_loss_pct"):
            if col in d.columns:
                raw = d[[col]].fillna(0)
                pieces.append(raw.rename(columns={col: f"{col}_mean_6"}))
                pieces.append(
                    pd.DataFrame({f"{col}_std_6": [0.0]}, index=d.index)
                )
        if not pieces:
            return pd.DataFrame()
        result = pd.concat(pieces, axis=1)
        result = result.select_dtypes(include=[np.number]).fillna(0).astype(np.float32)
        return result

    @staticmethod
    def _engineer_tti(df: pd.DataFrame) -> pd.DataFrame:
        """Engineer TTI features, preferring the module's own logic."""
        _tti_eng = None
        for _mod in ("models.tti_regressor_model", "ml.models.tti_regressor_model"):
            try:
                _tmp = __import__(_mod, fromlist=["engineer_features"])
                _tti_eng = getattr(_tmp, "engineer_features", None)
                if _tti_eng:
                    break
            except Exception:
                continue
        if _tti_eng:
            try:
                _r = _tti_eng(df)
                if _r.shape[1] == 24:
                    return _r
            except Exception:
                pass
        pieces: list[pd.DataFrame] = []
        tti_cols = [
            "cpu_util_pct", "memory_util_pct", "interface_bandwidth_util_pct",
            "latency_ms", "packet_loss_pct", "jitter_ms", "tcp_retransmits_pct",
            "bgp_prefix_count", "ospf_lsa_count", "ldp_label_count",
            "mpls_label_stack_depth", "flow_count",
        ]
        available = [c for c in tti_cols if c in df.columns]
        if not available:
            available = df.columns.tolist()
        pieces.append(df[available].fillna(0))
        # delta_3h features — not available for single-sample inference
        for c in ("cpu_util_pct", "latency_ms", "packet_loss_pct", "interface_bandwidth_util_pct", "bgp_prefix_count"):
            pieces.append(pd.DataFrame({f"delta_3h_{c}": [0.0]}, dtype=np.float64, index=df.index))
        # rolling stats — single sample = raw
        for c in ("latency_ms", "packet_loss_pct"):
            if c in df.columns:
                pieces.append(pd.DataFrame({f"{c}_rolling_mean_6": [float(df[c].iloc[-1])]}, dtype=np.float64, index=df.index))
                pieces.append(pd.DataFrame({f"{c}_rolling_std_6": [0.0]}, dtype=np.float64, index=df.index))
        # role dummies — default to 0 (unknown)
        for role in ("CE", "PE", "P"):
            pieces.append(pd.DataFrame({f"role_{role}": [0.0]}, dtype=np.float64, index=df.index))
        result = pd.concat(pieces, axis=1)
        result = result.fillna(0).astype(np.float32)
        return result

    # ── Predict fault ────────────────────────────────────────────────────

    def predict_fault(
        self, X: np.ndarray, timestamp_features: dict | None = None
    ) -> dict:
        """Run fault detection ensemble: majority vote across 4+ models.

        Parameters
        ----------
        X : np.ndarray
            Telemetry sample(s). Shape (n_features,) or (1, n_features).
        timestamp_features : dict, optional
            Extra context: 'timestamp' (str), 'device_id' (str),
            per-node features for GNN, time-series for Prophet.

        Returns
        -------
        dict with keys: fault_detected, fault_type, confidence,
                        probabilities, ensemble_vote
        """
        X = np.atleast_2d(np.asarray(X, dtype=np.float32))
        n_samples = X.shape[0]
        if n_samples == 0:
            return self._empty_fault_result()

        # Build DataFrame for feature engineering
        if X.shape[1] == len(COMMON_FEATURES):
            columns = COMMON_FEATURES
        elif X.shape[1] == len(XGB_FEATURE_NAMES):
            columns = XGB_FEATURE_NAMES
        else:
            columns = [f"f{i}" for i in range(X.shape[1])]

        df = pd.DataFrame(X, columns=columns[: X.shape[1]])

        # Load models
        xgb_model = self.load_model("xgboost")
        if_model = self.load_model("isolation_forest")
        ae_model = self.load_model("autoencoder")
        gnn_model = self.load_model("gnn")
        prophet_model = self.load_model("prophet")

        votes: dict[str, str] = {}

        #  ── 1) XGBoost vote ──────────────────────────────────────────
        xgb_vote = "none"
        xgb_probs: list[float] = [0.0] * len(FAULT_CLASSES_SORTED)
        if xgb_model is not None:
            try:
                xgb_df = df[COMMON_FEATURES] if all(c in df.columns for c in COMMON_FEATURES) else self._map_xgb_features(df)
                eng_df = self._engineer_xgboost(xgb_df)

                if xgb_model["engine"] == "onnx":
                    input_name = xgb_model["session"].get_inputs()[0].name
                    onnx_out = xgb_model["session"].run(
                        None, {input_name: eng_df.values.astype(np.float32)}
                    )
                    raw_probs = onnx_out[0]
                else:
                    native = xgb_model["model"]
                    raw_probs = native.predict_proba(eng_df)

                if raw_probs.ndim == 2 and raw_probs.shape[0] > 0:
                    xgb_probs = raw_probs[0].tolist()
                    class_idx = int(np.argmax(raw_probs[0]))
                    if class_idx < len(FAULT_CLASSES_SORTED):
                        xgb_vote = FAULT_CLASSES_SORTED[class_idx]
            except Exception as exc:
                self._warnings.append(f"XGBoost inference failed: {exc}")
        if xgb_model is not None:
            votes["xgboost"] = xgb_vote

        #  ── 2) IsolationForest vote ─────────────────────────────────
        if_vote = "none"
        if if_model is not None:
            try:
                if_df = self._engineer_isolation(df)

                if if_model["engine"] == "onnx" and len(if_df) > 0:
                    input_name = if_model["session"].get_inputs()[0].name
                    scores = if_model["session"].run(
                        None, {input_name: if_df.values.astype(np.float32)}
                    )[0]
                elif if_model["engine"] == "native" and len(if_df) > 0:
                    native = if_model["model"]
                    scores = native.decision_function(if_df)
                else:
                    scores = np.array([0.0])

                anomaly_score = float(np.mean(scores))
                if_vote = "anomaly" if anomaly_score < 0 else "none"
            except Exception as exc:
                self._warnings.append(f"IsolationForest inference failed: {exc}")
        if if_model is not None:
            votes["isolation_forest"] = if_vote

        #  ── 3) Autoencoder vote ─────────────────────────────────────
        ae_vote = "none"
        if ae_model is not None:
            try:
                ae_input_df = df[[c for c in AE_FEATURES if c in df.columns]]
                if len(ae_input_df.columns) == 0:
                    ae_input_df = pd.DataFrame(
                        np.zeros((n_samples, len(AE_FEATURES))),
                        columns=AE_FEATURES,
                    )

                input_vals = ae_input_df.values.astype(np.float32)

                if ae_model["engine"] == "onnx":
                    input_name = ae_model["session"].get_inputs()[0].name
                    recon = ae_model["session"].run(
                        None, {input_name: input_vals}
                    )[0]
                else:
                    scaler = ae_model.get("scaler")
                    if scaler is not None:
                        normed = scaler.transform(input_vals).astype(np.float32)
                    else:
                        normed = input_vals
                    device = self.device
                    t = torch.from_numpy(normed).to(device)
                    with torch.no_grad():
                        recon_t = ae_model["model"](t)
                    recon = recon_t.cpu().numpy()

                recon_err = float(np.mean((input_vals - recon) ** 2))
                threshold = 0.1
                ae_vote = "anomaly" if recon_err > threshold else "none"
            except Exception as exc:
                self._warnings.append(f"Autoencoder inference failed: {exc}")
        if ae_model is not None:
            votes["autoencoder"] = ae_vote

        #  ── 4) GNN vote ─────────────────────────────────────────────
        gnn_vote = "none"
        if gnn_model is not None:
            try:
                per_node = (
                    timestamp_features or {}
                )
                node_feats = self._build_gnn_features(per_node, df)
                A = _build_adjacency()
                A_hat = _normalize_adj(A)

                if gnn_model["engine"] == "onnx":
                    input_name = gnn_model["session"].get_inputs()[0].name
                    adj_name = gnn_model["session"].get_inputs()[1].name
                    embeddings = gnn_model["session"].run(
                        None,
                        {
                            input_name: node_feats.astype(np.float32),
                            adj_name: A_hat.astype(np.float32),
                        },
                    )[0]
                    mean_score = float(np.mean(np.abs(embeddings)))
                else:
                    device = self.device
                    t_feats = torch.from_numpy(node_feats).float().to(device)
                    t_A = torch.from_numpy(A_hat).float().to(device)
                    with torch.no_grad():
                        _, scores = gnn_model["model"](t_feats, t_A)
                    mean_score = float(scores.mean().cpu())

                gnn_vote = "anomaly" if mean_score > 0.5 else "none"
            except Exception as exc:
                self._warnings.append(f"GNN inference failed: {exc}")
        if gnn_model is not None:
            votes["gnn"] = gnn_vote

        #  ── 5) Prophet vote (time-series anomaly) ───────────────────
        prophet_vote = "none"
        if prophet_model is not None and timestamp_features is not None:
            try:
                series = self._build_prophet_series(timestamp_features, df)
                if series is not None and len(series) >= 48:
                    result = _seasonal_decompose(
                        series, model="additive", period=24
                    )
                    residual = result.resid.dropna()
                    if len(residual) >= 2:
                        z_scores = (
                            (residual - residual.mean()) / residual.std()
                        )
                        n_anomalies = int((z_scores.abs() > 3.0).sum())
                        prophet_vote = (
                            "anomaly" if n_anomalies > 0 else "none"
                        )
            except Exception as exc:
                self._warnings.append(f"Prophet inference failed: {exc}")
        if prophet_model is not None:
            votes["prophet"] = prophet_vote

        # ── Majority voting ────────────────────────────────────────────
        anomaly_votes = [
            k
            for k, v in votes.items()
            if v not in ("none", "")
        ]
        active_models = len(votes)
        n_anomaly = len(anomaly_votes)
        fault_detected = n_anomaly > (active_models // 2) if active_models > 0 else False

        # Determine fault type from XGBoost most likely class
        fault_type = xgb_vote
        if fault_detected and fault_type == "none":
            fault_type = "anomaly_detected"

        # Confidence from vote fraction
        confidence = round(n_anomaly / max(active_models, 1), 4) if active_models > 0 else 0.0

        # Probabilities from XGBoost, extended to all fault labels
        probabilities: dict[str, float] = {}
        for i, cls_name in enumerate(FAULT_CLASSES_SORTED):
            prob = xgb_probs[i] if i < len(xgb_probs) else 0.0
            probabilities[cls_name] = round(prob, 6)

        return {
            "fault_detected": fault_detected,
            "fault_type": fault_type,
            "confidence": confidence,
            "probabilities": probabilities,
            "ensemble_vote": votes,
        }

    def _empty_fault_result(self) -> dict:
        return {
            "fault_detected": False,
            "fault_type": "none",
            "confidence": 0.0,
            "probabilities": {c: 0.0 for c in FAULT_CLASSES_SORTED},
            "ensemble_vote": {},
        }

    @staticmethod
    def _map_xgb_features(df: pd.DataFrame) -> pd.DataFrame:
        """Map available telemetry columns to XGBoost expected names."""
        mapped: dict[str, float] = {}
        for xgb_col, common_col in XGB_TO_COMMON.items():
            if common_col and common_col in df.columns:
                mapped[xgb_col] = float(df[common_col].iloc[0])
            elif xgb_col in df.columns:
                mapped[xgb_col] = float(df[xgb_col].iloc[0])
            else:
                mapped[xgb_col] = 0.0
        return pd.DataFrame([mapped])

    @staticmethod
    def _build_gnn_features(
        ts_features: dict, df: pd.DataFrame
    ) -> np.ndarray:
        """Build (N_nodes, 7) feature matrix for GNN."""
        n = len(GNN_NODE_NAMES)
        feats = np.zeros((n, 7), dtype=np.float32)

        for i, node in enumerate(GNN_NODE_NAMES):
            feats[i] = [
                ts_features.get(f"{node}_latency", 0.0),
                ts_features.get(f"{node}_packet_loss", 0.0),
                ts_features.get(f"{node}_cpu", 0.0),
                ts_features.get(f"{node}_bandwidth", 0.0),
                ts_features.get(f"{node}_bgp_prefix", 0.0),
                ts_features.get(f"{node}_mpls_depth", 0.0),
                ts_features.get(f"{node}_tcp_retrans", 0.0),
            ]

        return feats

    @staticmethod
    def _build_prophet_series(
        ts_features: dict, df: pd.DataFrame
    ) -> Optional[pd.Series]:
        """Build a time-indexed series for Prophet decomposition.

        Uses 'latency_ms' from timestamp_features['timeseries'] if available,
        otherwise falls back to df.
        """
        series_data = ts_features.get("timeseries")
        if series_data is not None and isinstance(series_data, (list, np.ndarray)):
            n = len(series_data)
            index = pd.date_range(
                end=pd.Timestamp.now(), periods=n, freq="h"
            )
            return pd.Series(np.asarray(series_data, dtype=np.float64), index=index)

        if "latency_ms" in df.columns and len(df) >= 48:
            vals = df["latency_ms"].values.astype(np.float64)
            index = pd.date_range(
                end=pd.Timestamp.now(), periods=len(vals), freq="h"
            )
            return pd.Series(vals, index=index)

        return None

    # ── Predict time-series ──────────────────────────────────────────────

    def predict_timeseries(
        self, sequence: np.ndarray, steps_ahead: int = 3
    ) -> dict:
        """Forecast telemetry metrics using weighted LSTM + Prophet ensemble.

        Parameters
        ----------
        sequence : np.ndarray
            Historical telemetry sequence, shape (seq_len, n_features).
        steps_ahead : int
            Number of steps to forecast (default 3).

        Returns
        -------
        dict with keys: predictions, anomaly_probability, confidence_interval
        """
        seq = np.atleast_2d(np.asarray(sequence, dtype=np.float32))
        if seq.ndim == 2 and seq.shape[0] < SEQ_LENGTH:
            seq = np.pad(
                seq,
                ((SEQ_LENGTH - seq.shape[0], 0), (0, 0)),
                mode="edge",
            )

        seq_len = seq.shape[0]
        n_feats = seq.shape[1]

        lstm_model = self.load_model("lstm")
        prophet_model = self.load_model("prophet")

        # Default: flat forecast (mean of last few values)
        default_forecast = {
            "latency_ms": [float(np.mean(seq[-3:, 0]))] * steps_ahead
            if n_feats > 0
            else [0.0] * steps_ahead,
            "packet_loss_pct": [float(np.mean(seq[-3:, 1]))] * steps_ahead
            if n_feats > 1
            else [0.0] * steps_ahead,
            "cpu_util_pct": [float(np.mean(seq[-3:, 2]))] * steps_ahead
            if n_feats > 2
            else [0.0] * steps_ahead,
            "interface_bandwidth_util_pct": [
                float(np.mean(seq[-3:, 3]))
            ]
            * steps_ahead
            if n_feats > 3
            else [0.0] * steps_ahead,
        }

        # Store individual forecasts for weighted averaging
        lstm_forecast: dict[str, list[float]] | None = None
        prophet_forecast: dict[str, list[float]] | None = None

        # ── LSTM forecast ────────────────────────────────────────────────
        if lstm_model is not None:
            try:
                input_seq = seq[-SEQ_LENGTH:].copy()
                if input_seq.shape[0] < SEQ_LENGTH:
                    input_seq = np.pad(
                        input_seq,
                        ((SEQ_LENGTH - input_seq.shape[0], 0), (0, 0)),
                        mode="edge",
                    )

                input_seq_3d = input_seq[np.newaxis, :, :].astype(np.float32)

                if lstm_model["engine"] == "onnx":
                    input_name = lstm_model["session"].get_inputs()[0].name
                    raw = lstm_model["session"].run(
                        None, {input_name: input_seq_3d}
                    )[0]
                else:
                    device = self.device
                    t_in = torch.from_numpy(input_seq_3d).to(device)
                    with torch.no_grad():
                        raw = lstm_model["model"](t_in).cpu().numpy()

                # raw shape: (1, steps_ahead, n_outputs)
                if raw.ndim == 3:
                    lstm_forecast = {}
                    for i, name in enumerate(LSTM_OUTPUTS):
                        vals = raw[0, :steps_ahead, i].tolist()
                        lstm_forecast[name] = vals
            except Exception as exc:
                self._warnings.append(f"LSTM forecast failed: {exc}")

        # ── Prophet forecast ──────────────────────────────────────────────
        if prophet_model is not None and _HAS_STATS:
            try:
                index = pd.date_range(
                    end=pd.Timestamp.now(),
                    periods=seq_len,
                    freq="h",
                )
                for target_name in LSTM_OUTPUTS:
                    col_idx = self._get_feature_index(target_name, n_feats)
                    if col_idx is None:
                        continue
                    series = pd.Series(
                        seq[:, col_idx].astype(np.float64), index=index
                    )
                    series = series.asfreq("h").ffill()

                    sarimax = _SARIMAX(
                        series,
                        order=(1, 0, 1),
                        seasonal_order=(1, 1, 1, 24),
                        enforce_stationarity=False,
                        enforce_invertibility=False,
                    )
                    fitted = sarimax.fit(disp=False, maxiter=200)
                    result = fitted.get_forecast(steps=steps_ahead)
                    pred = result.predicted_mean.values.tolist()

                    if prophet_forecast is None:
                        prophet_forecast = {}
                    prophet_forecast[target_name] = pred

            except Exception as exc:
                self._warnings.append(f"Prophet forecast failed: {exc}")

        # ── Weighted average ─────────────────────────────────────────────
        predictions: dict[str, list[float]] = {}
        confidence_interval: dict[str, tuple[float, float]] = {}

        lstm_weight = 0.6 if lstm_forecast else 0.0
        prophet_weight = 0.4 if prophet_forecast else 0.0

        for target in LSTM_OUTPUTS:
            if lstm_forecast and target in lstm_forecast:
                l_vals = lstm_forecast[target]
            else:
                l_vals = default_forecast.get(target, [0.0] * steps_ahead)

            if prophet_forecast and target in prophet_forecast:
                p_vals = prophet_forecast[target]
            else:
                p_vals = default_forecast.get(target, [0.0] * steps_ahead)

            # Pad to same length
            max_len = max(len(l_vals), len(p_vals), steps_ahead)
            l_vals = l_vals + [l_vals[-1]] * (max_len - len(l_vals)) if l_vals else [0.0] * max_len
            p_vals = p_vals + [p_vals[-1]] * (max_len - len(p_vals)) if p_vals else [0.0] * max_len

            total_w = lstm_weight + prophet_weight or 1.0
            combined = [
                (lstm_weight * l_vals[i] + prophet_weight * p_vals[i]) / total_w
                for i in range(steps_ahead)
            ]
            predictions[target] = [round(v, 6) for v in combined]

            # Confidence interval from per-step variance across models
            ci_lower: list[float] = []
            ci_upper: list[float] = []
            for i in range(steps_ahead):
                vals = []
                if lstm_forecast and i < len(l_vals):
                    vals.append(l_vals[i])
                if prophet_forecast and i < len(p_vals):
                    vals.append(p_vals[i])
                if vals:
                    mean_v = float(np.mean(vals))
                    std_v = float(np.std(vals)) if len(vals) > 1 else float(abs(mean_v) * 0.1 + 0.01)
                    ci_lower.append(round(mean_v - 1.96 * std_v, 6))
                    ci_upper.append(round(mean_v + 1.96 * std_v, 6))
                else:
                    ci_lower.append(0.0)
                    ci_upper.append(0.0)

            ci_lower_final = min(ci_lower) if ci_lower else 0.0
            ci_upper_final = max(ci_upper) if ci_upper else 0.0
            confidence_interval[target] = (ci_lower_final, ci_upper_final)

        # Anomaly probability based on forecast variance
        all_variances: list[float] = []
        for target in LSTM_OUTPUTS:
            if target in predictions:
                vals = predictions[target]
                if len(vals) > 1:
                    all_variances.append(float(np.var(vals)))

        anomaly_prob = min(1.0, float(np.mean(all_variances)) * 10) if all_variances else 0.0

        return {
            "predictions": predictions,
            "anomaly_probability": round(anomaly_prob, 6),
            "confidence_interval": confidence_interval,
        }

    @staticmethod
    def _get_feature_index(name: str, n_feats: int) -> int | None:
        """Map metric name to column index in the input sequence."""
        mapping = {
            "latency_ms": 0,
            "packet_loss_pct": 1,
            "cpu_util_pct": 2,
            "interface_bandwidth_util_pct": 3,
        }
        idx = mapping.get(name)
        if idx is not None and idx < n_feats:
            return idx
        return None

    # ── Predict TTI ──────────────────────────────────────────────────────

    def predict_tti(self, features: np.ndarray) -> dict:
        """Predict time-to-incident from current telemetry snapshot.

        Parameters
        ----------
        features : np.ndarray
            Telemetry feature vector, shape (n_features,) or (1, n_features).

        Returns
        -------
        dict with keys: hours_to_next_incident, predicted_severity,
                        fault_probability, confidence
        """
        feats = np.atleast_2d(np.asarray(features, dtype=np.float32))

        tti_model = self.load_model("tti_regressor")

        if tti_model is None:
            return {
                "hours_to_next_incident": float("inf"),
                "predicted_severity": 0.0,
                "fault_probability": 0.0,
                "confidence": 0.0,
            }

        try:
            # Build DataFrame for TTI feature engineering
            n_feats = feats.shape[1]
            if n_feats == len(COMMON_FEATURES):
                columns = COMMON_FEATURES
            elif n_feats == 12:
                columns = [
                    "cpu_util_pct",
                    "memory_util_pct",
                    "interface_bandwidth_util_pct",
                    "latency_ms",
                    "packet_loss_pct",
                    "jitter_ms",
                    "tcp_retransmits_pct",
                    "bgp_prefix_count",
                    "ospf_lsa_count",
                    "ldp_label_count",
                    "mpls_label_stack_depth",
                    "flow_count",
                ]
            else:
                columns = [f"f{i}" for i in range(n_feats)]

            df_in = pd.DataFrame(feats, columns=columns[:n_feats])

            # Engineer TTI features (simplified: raw + dummies)
            tti_df = self._engineer_tti(df_in)

            if tti_model["engine"] == "onnx":
                input_name = tti_model["session"].get_inputs()[0].name
                raw_pred = tti_model["session"].run(
                    None, {input_name: tti_df.values.astype(np.float32)}
                )[0]
                tree_variance = None
            else:
                native = tti_model["model"]
                raw_pred = native.predict(tti_df)

                # Tree variance as confidence proxy
                tree_preds = np.array(
                    [tree.predict(tti_df) for tree in native.estimators_]
                )
                tree_variance = float(np.mean(np.var(tree_preds, axis=0)))

            raw_pred = np.atleast_2d(raw_pred)

            hours = float(raw_pred[0, 0]) if raw_pred.shape[1] >= 1 else float("inf")
            severity = float(raw_pred[0, 1]) if raw_pred.shape[1] >= 2 else 0.0
            prob = float(raw_pred[0, 2]) if raw_pred.shape[1] >= 3 else 0.0

            # Confidence: inverse of variance, normalized
            if tree_variance is not None and tree_variance > 0:
                confidence = round(1.0 / (1.0 + tree_variance), 4)
            else:
                confidence = 0.5

            return {
                "hours_to_next_incident": round(hours, 4),
                "predicted_severity": round(severity, 4),
                "fault_probability": round(prob, 4),
                "confidence": min(max(confidence, 0.0), 1.0),
            }

        except Exception as exc:
            self._warnings.append(f"TTI inference failed: {exc}")
            return {
                "hours_to_next_incident": float("inf"),
                "predicted_severity": 0.0,
                "fault_probability": 0.0,
                "confidence": 0.0,
            }

    # ── Full diagnosis ───────────────────────────────────────────────────

    def full_diagnosis(
        self,
        df_current: pd.DataFrame,
        timeseries_history: np.ndarray,
    ) -> dict:
        """Run all 3 prediction pipelines and return combined diagnosis.

        Parameters
        ----------
        df_current : pd.DataFrame
            Current telemetry snapshot (single row or recent window).
        timeseries_history : np.ndarray
            Historical telemetry sequence, shape (T, n_features).

        Returns
        -------
        dict combining fault, timeseries, and TTI predictions.
        """
        # Extract only COMMON_FEATURES for the ML models
        common_present = [c for c in COMMON_FEATURES if c in df_current.columns]
        if common_present:
            current_array = df_current[common_present].values.astype(np.float32)
        else:
            numeric_cols = df_current.select_dtypes(include=[np.number]).columns
            current_array = df_current[numeric_cols].values.astype(np.float32)
        if current_array.ndim == 2:
            current_sample = current_array[-1:]
        else:
            current_sample = current_array

        # Build timestamp_features from DataFrame
        ts_features: dict = {}
        if "timestamp" in df_current.columns:
            ts_features["timestamp"] = str(df_current["timestamp"].iloc[-1])
        if "device_id" in df_current.columns:
            ts_features["device_id"] = str(df_current["device_id"].iloc[-1])

        # Check for per-node features needed by GNN
        for node in GNN_NODE_NAMES:
            for suffix in GNN_FEATURE_NAMES:
                col = f"{node}_{suffix}"
                if col in df_current.columns:
                    ts_features[col] = float(df_current[col].iloc[-1])

        # Time series data for prophet
        if "latency_ms" in df_current.columns:
            latency_vals = df_current["latency_ms"].values.tolist()
            if timeseries_history is not None and timeseries_history.ndim == 2:
                if timeseries_history.shape[1] > 0:
                    extra_vals = timeseries_history[:, 0].tolist()
                    latency_vals = extra_vals + latency_vals
            ts_features["timeseries"] = latency_vals

        # Run all 3 predictions
        fault_result = self.predict_fault(current_sample, ts_features)
        ts_result = self.predict_timeseries(timeseries_history)
        tti_result = self.predict_tti(current_sample)

        return {
            "fault_detection": fault_result,
            "time_series_forecast": ts_result,
            "tti_estimate": tti_result,
            "warnings": self._warnings[-20:],
        }

    # ── Export pipeline ──────────────────────────────────────────────────

    def export_pipeline(self, export_dir: str) -> str:
        """Export complete pipeline configuration as JSON.

        Parameters
        ----------
        export_dir : str
            Directory to write the pipeline config.

        Returns
        -------
        str
            Path to the written JSON file.
        """
        export_path = Path(export_dir)
        export_path.mkdir(parents=True, exist_ok=True)

        config = {
            "ensemble_predictor": "v1.0",
            "models": {},
            "voting_strategies": {
                "fault_detection": "majority_vote",
                "time_series_forecast": "weighted_average",
                "tti_estimate": "random_forest_uncertainty",
            },
            "available_models": [],
            "unavailable_models": [],
            "device": self.device,
        }

        for model_name in [
            "xgboost",
            "isolation_forest",
            "autoencoder",
            "gnn",
            "lstm",
            "prophet",
            "tti_regressor",
        ]:
            model = self.load_model(model_name)
            status = "loaded" if model is not None else "unavailable"
            engine = model["engine"] if model else None

            config["models"][model_name] = {
                "status": status,
                "engine": engine,
            }
            if model is not None:
                config["available_models"].append(model_name)
            else:
                config["unavailable_models"].append(model_name)

        config["warnings"] = self._warnings[-50:]

        filepath = export_path / "ensemble_pipeline.json"
        with open(filepath, "w") as f:
            json.dump(config, f, indent=2)

        return str(filepath)

    # ── Softmax utility ──────────────────────────────────────────────────

    @staticmethod
    def _softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
        return _softmax(x, axis)


# ═══════════════════════════════════════════════════════════════════════════
# main — demonstration with synthetic data
# ═══════════════════════════════════════════════════════════════════════════


def _generate_test_data() -> tuple[np.ndarray, np.ndarray]:
    """Generate synthetic telemetry data for testing."""
    rng = np.random.default_rng(42)

    # Single sample features
    n_features = len(COMMON_FEATURES)
    current = rng.exponential(scale=1.0, size=n_features).astype(np.float32)
    current[3] *= 5.0  # elevate latency
    current[4] += 3.0  # elevate packet loss

    # Time-series history
    T = 200
    history = rng.exponential(scale=1.0, size=(T, n_features)).astype(np.float32)

    return current, history


def main() -> None:
    print("=" * 60)
    print("  PS13 Ensemble Predictor — Unified Diagnosis Demo")
    print("=" * 60)

    # Generate test data
    print("\n[INFO] Generating synthetic test data...")
    current_sample, history = _generate_test_data()
    print(
        f"[INFO] Current sample: {current_sample.shape}, "
        f"History: {history.shape}"
    )

    # Initialize predictor
    print("\n[INFO] Initializing EnsemblePredictor...")
    predictor = EnsemblePredictor()

    # Run fault detection
    print("\n" + "-" * 60)
    print("  1) FAULT DETECTION")
    print("-" * 60)
    try:
        fault_result = predictor.predict_fault(current_sample)
        print(f"   Fault detected : {fault_result['fault_detected']}")
        print(f"   Fault type     : {fault_result['fault_type']}")
        print(f"   Confidence     : {fault_result['confidence']:.4f}")
        print(f"   Ensemble vote  :")
        for model_name, vote in fault_result["ensemble_vote"].items():
            print(f"     {model_name:<20s}: {vote}")
    except Exception as exc:
        print(f"   [ERROR] Fault detection failed: {exc}")

    # Run time-series forecast
    print("\n" + "-" * 60)
    print("  2) TIME-SERIES FORECAST")
    print("-" * 60)
    try:
        ts_result = predictor.predict_timeseries(history, steps_ahead=3)
        print(f"   Predictions:")
        for metric, vals in ts_result["predictions"].items():
            print(f"     {metric:<35s}: {vals}")
        print(f"   Anomaly prob   : {ts_result['anomaly_probability']:.6f}")
        print(f"   Confidence intervals:")
        for metric, (lo, hi) in ts_result["confidence_interval"].items():
            print(f"     {metric:<35s}: ({lo:.4f}, {hi:.4f})")
    except Exception as exc:
        print(f"   [ERROR] Time-series forecast failed: {exc}")

    # Run TTI estimate
    print("\n" + "-" * 60)
    print("  3) TIME-TO-INCIDENT ESTIMATE")
    print("-" * 60)
    try:
        tti_result = predictor.predict_tti(current_sample)
        print(f"   Hours to next incident : {tti_result['hours_to_next_incident']}")
        print(f"   Predicted severity     : {tti_result['predicted_severity']:.4f}")
        print(f"   Fault probability      : {tti_result['fault_probability']:.4f}")
        print(f"   Confidence             : {tti_result['confidence']:.4f}")
    except Exception as exc:
        print(f"   [ERROR] TTI estimate failed: {exc}")

    # Unified diagnosis
    print("\n" + "=" * 60)
    print("  UNIFIED DIAGNOSIS (full_diagnosis)")
    print("=" * 60)
    df_current = pd.DataFrame(
        [current_sample],
        columns=COMMON_FEATURES,
    )
    try:
        diagnosis = predictor.full_diagnosis(
            df_current=df_current, timeseries_history=history
        )
        fd = diagnosis["fault_detection"]
        print(f"   Fault detected  : {fd['fault_detected']}")
        print(f"   Fault type      : {fd['fault_type']}")
        print(f"   Fault confidence: {fd['confidence']:.4f}")
        print(
            f"   TTI estimate    : "
            f"{diagnosis['tti_estimate']['hours_to_next_incident']} hours"
        )
        print(
            f"   TTI confidence  : "
            f"{diagnosis['tti_estimate']['confidence']:.4f}"
        )
    except Exception as exc:
        print(f"   [ERROR] Full diagnosis failed: {exc}")

    # Export pipeline
    print(f"\n[INFO] Exporting pipeline config...")
    try:
        export_path = predictor.export_pipeline("ml/models")
        print(f"[INFO] Pipeline config written to {export_path}")
    except Exception as exc:
        print(f"[WARN] Pipeline export failed: {exc}")

    # Warnings summary
    if predictor._warnings:
        print(f"\n[WARN] Model loading warnings ({len(predictor._warnings)}):")
        for w in predictor._warnings[-5:]:
            print(f"  - {w}")

    print("\n" + "=" * 60)
    print("  [DONE] Ensemble predictor demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
