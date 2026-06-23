"""
XGBoost-based fault classification model for network telemetry.
Part of PS13 predictive SD-WAN NOC ensemble.
"""

from __future__ import annotations

import json
import os
import warnings
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

FAULT_CLASSES = [
    "none",
    "link_fail",
    "bgp_flap",
    "congestion",
    "route_leak",
    "crc_errors",
    "node_crash",
    "lsp_break",
]

TELEMETRY_FEATURES = [
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


def _generate_synthetic_data(n_samples: int = 10000) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    data: dict[str, np.ndarray] = {}

    for col in TELEMETRY_FEATURES:
        data[col] = rng.exponential(scale=1.0, size=n_samples).astype(np.float32)

    df = pd.DataFrame(data)

    fault_series = rng.choice(FAULT_CLASSES, size=n_samples, p=[
        0.30, 0.15, 0.10, 0.15, 0.08, 0.07, 0.10, 0.05,
    ])

    mask_link = fault_series == "link_fail"
    df.loc[mask_link, "latency_ms"] *= 8.0
    df.loc[mask_link, "packet_loss_pct"] += rng.uniform(5, 25, size=mask_link.sum())

    mask_bgp = fault_series == "bgp_flap"
    df.loc[mask_bgp, "bgp_prefix_count"] += rng.uniform(50, 200, size=mask_bgp.sum()).astype(int)

    mask_cong = fault_series == "congestion"
    df.loc[mask_cong, "interface_bandwidth_util_pct"] *= 2.5
    df.loc[mask_cong, "latency_ms"] *= 3.0
    df.loc[mask_cong, "jitter_ms"] *= 4.0

    mask_route = fault_series == "route_leak"
    df.loc[mask_route, "bgp_prefix_count"] += rng.uniform(100, 500, size=mask_route.sum()).astype(int)
    df.loc[mask_route, "latency_ms"] *= 1.5

    mask_crc = fault_series == "crc_errors"
    df.loc[mask_crc, "tcp_retransmits_pct"] += rng.uniform(5, 20, size=mask_crc.sum())
    df.loc[mask_crc, "packet_loss_pct"] += rng.uniform(1, 10, size=mask_crc.sum())

    mask_crash = fault_series == "node_crash"
    df.loc[mask_crash, "interface_bandwidth_util_pct"] *= 0.05
    df.loc[mask_crash, "latency_ms"] *= 10.0
    df.loc[mask_crash, "packet_loss_pct"] += rng.uniform(50, 100, size=mask_crash.sum())

    mask_lsp = fault_series == "lsp_break"
    df.loc[mask_lsp, "interface_bandwidth_util_pct"] *= 0.3
    df.loc[mask_lsp, "packet_loss_pct"] += rng.uniform(10, 40, size=mask_lsp.sum())

    df["fault_type"] = fault_series
    return df


def _ensure_data_exists(path: Path) -> Path:
    if path.exists():
        return path
    warnings.warn(f"{path} not found — generating synthetic data")
    df = _generate_synthetic_data()
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    return path


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    pieces: list[pd.DataFrame] = [df[numeric_cols]]

    for col in numeric_cols:
        s = df[col]
        eng = pd.DataFrame({
            f"{col}_lag_1": s.shift(1).fillna(0),
            f"{col}_rolling_mean_6": s.rolling(window=6, min_periods=1).mean().fillna(0),
            f"{col}_rolling_std_6": s.rolling(window=6, min_periods=1).std().fillna(0),
            f"{col}_delta": s.diff(1).fillna(0),
        })
        pieces.append(eng)

    return pd.concat(pieces, axis=1)


def prepare_features(
    df: pd.DataFrame, label_encoder: LabelEncoder | None = None
) -> Tuple[pd.DataFrame, np.ndarray, LabelEncoder]:
    raw = df.copy()

    if "fault_type" not in raw.columns:
        raise ValueError("DataFrame must contain 'fault_type' column")

    y_raw = raw.pop("fault_type").values

    if label_encoder is None:
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y_raw)
    else:
        y = label_encoder.transform(y_raw)

    # Strip pre-existing engineered columns; keep only raw TELEMETRY_FEATURES
    raw = raw[[c for c in TELEMETRY_FEATURES if c in raw.columns]]
    raw = engineer_features(raw)

    numeric_cols = raw.select_dtypes(include=[np.number]).columns.tolist()
    X = raw[numeric_cols].fillna(0).astype(np.float32)

    return X, y, label_encoder


def train_model(
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    X_val: pd.DataFrame,
    y_val: np.ndarray,
) -> xgb.XGBClassifier:
    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=8,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="mlogloss",
        early_stopping_rounds=20,
        random_state=42,
        verbosity=1,
    )

    model.fit(
        X_train,
        y_train,
        eval_set=[(X_train, y_train), (X_val, y_val)],
        verbose=True,
    )

    return model


def predict(
    model: xgb.XGBClassifier, X: pd.DataFrame
) -> Tuple[np.ndarray, np.ndarray]:
    classes = model.predict(X)
    probs = model.predict_proba(X)
    return classes, probs


def export_to_onnx(model: xgb.XGBClassifier, filepath: str | Path) -> None:
    try:
        import onnxmltools
        from skl2onnx.common.data_types import FloatTensorType
    except ImportError:
        try:
            import treelite  # noqa: F401
            import treelite_runtime  # noqa: F401
        except ImportError:
            raise ImportError(
                "ONNX export requires either 'onnxmltools' or 'treelite'. "
                "Install with: pip install onnxmltools skl2onnx"
            )

    n_features = model.n_features_in_

    initial_types = [("input", FloatTensorType([None, n_features]))]
    onnx_model = onnxmltools.convert_xgboost(model, initial_types=initial_types)

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(onnx_model.SerializeToString())


def get_feature_importance(
    model: xgb.XGBClassifier, feature_names: list[str]
) -> dict[str, float]:
    importance = model.feature_importances_
    return dict(zip(feature_names, [round(float(v), 6) for v in importance]))


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    data_path = _ensure_data_exists(base / "data" / "telemetry.parquet")

    print(f"[INFO] Loading data from {data_path}")
    df = pd.read_parquet(data_path)
    print(f"[INFO] Loaded {len(df)} rows, {len(df.columns)} columns")

    X, y, label_encoder = prepare_features(df)
    feature_names = X.columns.tolist()
    print(f"[INFO] Feature matrix: {X.shape}")
    print(f"[INFO] Classes: {label_encoder.classes_.tolist()}")

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"[INFO] Train: {len(X_train)}, Validation: {len(X_val)}")

    model = train_model(X_train, y_train, X_val, y_val)

    y_pred, y_proba = predict(model, X_val)
    acc = accuracy_score(y_val, y_pred)
    print(f"\n[RESULT] Validation accuracy: {acc:.4f}\n")

    report = classification_report(
        y_val,
        y_pred,
        target_names=label_encoder.classes_.tolist(),
        digits=4,
    )
    print(report)

    checkpoint_dir = base / "models" / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    model_path = checkpoint_dir / "xgboost.json"
    model.save_model(str(model_path))
    print(f"[INFO] Model saved to {model_path}")

    onnx_dir = base / "models" / "onnx"
    onnx_dir.mkdir(parents=True, exist_ok=True)
    onnx_path = onnx_dir / "xgboost.onnx"
    try:
        export_to_onnx(model, onnx_path)
        print(f"[INFO] ONNX exported to {onnx_path}")
    except ImportError as e:
        print(f"[WARN] ONNX export skipped: {e}")

    importance = get_feature_importance(model, feature_names)
    top_k = sorted(importance.items(), key=lambda x: -x[1])[:10]
    print("\n[INFO] Top 10 features by importance:")
    for name, score in top_k:
        print(f"  {name}: {score:.6f}")


if __name__ == "__main__":
    main()
