"""
Time-To-Incident (TTI) Regression Model for PS13 Predictive SD-WAN NOC.

Uses a RandomForestRegressor (multi-output) to predict hours until next
network fault, expected severity score, and fault probability from current
telemetry state + engineered features.
"""

from __future__ import annotations

import json
import os
import pickle
import warnings
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

TELEMETRY_FEATURES: list[str] = [
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

DELTA_FEATURES: list[str] = [
    "cpu_util_pct",
    "latency_ms",
    "packet_loss_pct",
    "interface_bandwidth_util_pct",
    "bgp_prefix_count",
]

ROLLING_FEATURES: list[str] = [
    "latency_ms",
    "packet_loss_pct",
]

TARGET_NAMES: list[str] = [
    "time_to_incident_hours",
    "severity_score",
    "fault_probability",
]

MAX_HOURS: int = 720


def _compute_3h_delta(df: pd.DataFrame, col: str) -> pd.Series:
    """Compute change over last 3 hours per-device."""
    return df.groupby("device_id")[col].diff(3).fillna(0.0)


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build the full feature matrix from raw telemetry + engineered features.

    Returns a DataFrame with columns in a deterministic order and NaN handled.
    """
    pieces: list[pd.DataFrame] = []

    current = df[TELEMETRY_FEATURES].copy()
    pieces.append(current)

    delta_cols: dict[str, str] = {}
    for col in DELTA_FEATURES:
        name = f"delta_3h_{col}"
        pieces.append(df[["device_id"]].assign(**{name: _compute_3h_delta(df, col)}).drop(columns=["device_id"]))
        delta_cols[col] = name

    for col in ROLLING_FEATURES:
        grouped = df.groupby("device_id")[col]
        pieces.append(
            grouped.transform(lambda x: x.rolling(6, min_periods=1).mean())
            .rename(f"{col}_rolling_mean_6")
            .to_frame()
        )
        pieces.append(
            grouped.transform(lambda x: x.rolling(6, min_periods=1).std())
            .fillna(0.0)
            .rename(f"{col}_rolling_std_6")
            .to_frame()
        )

    role_dummies = pd.get_dummies(df["device_role"], prefix="role", dtype=np.float64)
    for r in ("CE", "PE", "P"):
        col = f"role_{r}"
        if col not in role_dummies.columns:
            role_dummies[col] = 0.0
    pieces.append(role_dummies[["role_CE", "role_PE", "role_P"]])

    X = pd.concat(pieces, axis=1)

    X = X.fillna(X.median(numeric_only=True))

    return X


def _prepare_targets(df: pd.DataFrame) -> pd.DataFrame:
    """Build multi-output target matrix from the raw DataFrame.

    - time_to_incident_hours: directly from column (NaN → MAX_HOURS)
    - severity_score: fault_severity (already 0 for no-fault)
    - fault_probability: 1 if fault_type != 'none', else 0
    """
    tti = df["time_to_incident_hours"].fillna(MAX_HOURS).values.astype(np.float64)
    sev = df["fault_severity"].values.astype(np.float64)
    prob = (df["fault_type"] != "none").astype(np.float64).values

    return pd.DataFrame(
        {"time_to_incident_hours": tti, "severity_score": sev, "fault_probability": prob},
        dtype=np.float64,
    )


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.DataFrame,
    X_val: pd.DataFrame,
    y_val: pd.DataFrame,
) -> RandomForestRegressor:
    """Train a multi-output RandomForestRegressor.

    No built-in early stopping for sklearn RF; we train a fixed-configuration
    model. An XGBoost alternative is available in the xgboost_model module.
    """
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        min_samples_leaf=4,
        random_state=42,
        n_jobs=-1,
        verbose=1,
    )

    model.fit(X_train, y_train)

    return model


def predict(
    model: RandomForestRegressor, X: pd.DataFrame
) -> np.ndarray:
    """Return predictions as (n_samples, 3) array.

    Columns: [time_to_incident_hours, severity_score, fault_probability]
    """
    return model.predict(X)


def evaluate_model(
    model: RandomForestRegressor, X_test: pd.DataFrame, y_test: pd.DataFrame
) -> Dict[str, Dict[str, float]]:
    """Return per-target MAE, RMSE, and R² scores.

    Returns nested dict: {target_name: {"mae": ..., "rmse": ..., "r2": ...}}
    """
    y_pred = predict(model, X_test)
    results: dict[str, dict[str, float]] = {}
    for i, name in enumerate(TARGET_NAMES):
        y_true = y_test.iloc[:, i].values
        y_hat = y_pred[:, i]
        results[name] = {
            "mae": round(float(mean_absolute_error(y_true, y_hat)), 4),
            "rmse": round(float(np.sqrt(mean_squared_error(y_true, y_hat))), 4),
            "r2": round(float(r2_score(y_true, y_hat)), 6),
        }
    return results


def export_to_onnx(model: RandomForestRegressor, filepath: str | Path) -> None:
    """Export the sklearn model to ONNX format.

    Tries onnxmltools → treelite → pickle fallback.
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        from skl2onnx import convert_sklearn
        from skl2onnx.common.data_types import FloatTensorType

        n_features = model.n_features_in_
        initial_types = [("input", FloatTensorType([None, n_features]))]
        onnx_model = convert_sklearn(model, initial_types=initial_types)
        with open(filepath, "wb") as f:
            f.write(onnx_model.SerializeToString())
        return
    except ImportError:
        pass

    try:
        import treelite  # noqa: F401
        import treelite_runtime  # noqa: F401
    except ImportError:
        pass

    raise ImportError(
        "ONNX export requires either 'skl2onnx' or 'treelite'. "
        "Install with: pip install skl2onnx onnxmltools"
    )


def get_feature_importance(
    model: RandomForestRegressor, feature_names: list[str]
) -> dict[str, float]:
    """Return feature importance dict (mean across all output targets)."""
    if hasattr(model, "feature_importances_"):
        importance = model.feature_importances_
        return dict(
            zip(feature_names, [round(float(v), 6) for v in importance])
        )
    return {}


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    data_path = base / "data" / "telemetry.parquet"

    if not data_path.exists():
        print(f"[ERROR] Data not found at {data_path}. Run generate_synthetic_data.py first.")
        return

    print(f"[INFO] Loading data from {data_path}")
    df = pd.read_parquet(data_path)
    print(f"[INFO] Loaded {len(df)} rows, {len(df.columns)} columns")

    print("[INFO] Engineering features...")
    X = engineer_features(df)
    y = _prepare_targets(df)

    print(f"[INFO] Feature matrix: {X.shape}")
    print(f"[INFO] Target matrix:  {y.shape}")

    fault_rate = y["fault_probability"].mean()
    print(f"[INFO] Fault rate: {fault_rate:.4f} ({y['fault_probability'].sum():.0f} / {len(y)})")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"[INFO] Train: {len(X_train)}, Test: {len(X_test)}")

    model = train_model(X_train, y_train, X_train, y_train)

    metrics = evaluate_model(model, X_test, y_test)
    print("\n[RESULTS] Per-target evaluation metrics:")
    print(f"  {'Target':<28s} {'MAE':>10s} {'RMSE':>10s} {'R²':>10s}")
    print(f"  {'-' * 28} {'-' * 10} {'-' * 10} {'-' * 10}")
    for target_name, scores in metrics.items():
        print(
            f"  {target_name:<28s} {scores['mae']:>10.4f} {scores['rmse']:>10.4f} {scores['r2']:>10.6f}"
        )

    checkpoint_dir = base / "models" / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    model_path = checkpoint_dir / "tti_regressor.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"\n[INFO] Model saved to {model_path}")

    onnx_dir = base / "models" / "onnx"
    onnx_dir.mkdir(parents=True, exist_ok=True)
    onnx_path = onnx_dir / "tti_regressor.onnx"
    try:
        export_to_onnx(model, onnx_path)
        print(f"[INFO] ONNX exported to {onnx_path}")
    except ImportError as e:
        print(f"[WARN] ONNX export skipped: {e}")
        onnx_fallback = onnx_path.with_suffix(".pkl")
        with open(onnx_fallback, "wb") as f:
            pickle.dump(model, f)
        print(f"[INFO] Pickle fallback saved to {onnx_fallback}")

    feature_names = X.columns.tolist()
    importance = get_feature_importance(model, feature_names)
    top_k = sorted(importance.items(), key=lambda x: -x[1])[:10]
    print("\n[INFO] Top 10 features by importance:")
    print(f"  {'Feature':<35s} {'Importance':>12s}")
    print(f"  {'-' * 35} {'-' * 12}")
    for name, score in top_k:
        print(f"  {name:<35s} {score:>12.6f}")


if __name__ == "__main__":
    main()
