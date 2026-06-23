"""
IsolationForest-based unsupervised anomaly detection for network telemetry.
Part of PS13 predictive SD-WAN NOC ensemble — detects anomalies without
requiring labeled data.
"""

from __future__ import annotations

import pickle
import warnings
from pathlib import Path
from typing import Any, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

RAW_FEATURES = [
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

SITE_AGG_FEATURES = [
    "cpu_util_pct",
    "memory_util_pct",
    "interface_bandwidth_util_pct",
    "latency_ms",
    "packet_loss_pct",
    "jitter_ms",
]

ROLLING_WINDOW = 6


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in RAW_FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Missing raw feature columns: {missing}")

    pieces: list[pd.DataFrame] = [df[RAW_FEATURES].copy()]

    if "site" in df.columns:
        site_means = (
            df.groupby("site")[SITE_AGG_FEATURES]
            .transform("mean")
            .rename(columns={c: f"site_mean_{c}" for c in SITE_AGG_FEATURES})
        )
        pieces.append(site_means)

    sorted_df = df.sort_values(["device_id", "hour"]).reset_index(drop=True) if all(
        c in df.columns for c in ("device_id", "hour")
    ) else df

    for col in ("latency_ms", "packet_loss_pct"):
        if col not in df.columns:
            continue
        grouped = sorted_df.groupby("device_id")[col] if "device_id" in sorted_df.columns else sorted_df[col]
        mean_series = grouped.transform(
            lambda x: x.rolling(ROLLING_WINDOW, min_periods=1).mean()
        ).fillna(0)
        std_series = grouped.transform(
            lambda x: x.rolling(ROLLING_WINDOW, min_periods=1).std()
        ).fillna(0)
        pieces.append(mean_series.rename(f"{col}_mean_6"))
        pieces.append(std_series.rename(f"{col}_std_6"))

    result = pd.concat(pieces, axis=1)
    result = result.select_dtypes(include=[np.number]).fillna(0).astype(np.float32)
    return result


def train_model(feature_matrix: pd.DataFrame) -> IsolationForest:
    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        max_samples="auto",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(feature_matrix)
    return model


def predict_anomaly(
    model: IsolationForest, feature_matrix: pd.DataFrame
) -> Tuple[np.ndarray, np.ndarray]:
    predictions = model.predict(feature_matrix)
    scores = model.decision_function(feature_matrix)
    return predictions, scores


def get_anomaly_summary(
    original_df: pd.DataFrame,
    predictions: np.ndarray,
    scores: np.ndarray,
) -> pd.DataFrame:
    result = original_df.copy()
    result["prediction"] = predictions
    result["anomaly_score"] = scores
    result["is_anomaly"] = predictions == -1

    anomalies = result[result["is_anomaly"]]
    if len(anomalies) == 0:
        return pd.DataFrame(columns=[
            "device_id", "site", "anomaly_count", "mean_anomaly_score",
            "mean_latency_ms", "mean_packet_loss_pct", "mean_cpu_util_pct",
        ])

    summary = anomalies.groupby("device_id", sort=False).agg(
        site=("site", "first"),
        anomaly_count=("is_anomaly", "count"),
        mean_anomaly_score=("anomaly_score", "mean"),
        std_anomaly_score=("anomaly_score", "std"),
        mean_latency_ms=("latency_ms", "mean"),
        mean_packet_loss_pct=("packet_loss_pct", "mean"),
        mean_cpu_util_pct=("cpu_util_pct", "mean"),
    ).reset_index()

    return summary.sort_values("mean_anomaly_score")


def export_to_onnx(model: IsolationForest, filepath: str | Path) -> None:
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    try:
        from hummingbird.ml import convert as hb_convert

        hb_model = hb_convert(model, "onnx")
        hb_model.save(str(filepath))
        return
    except ImportError:
        pass

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

    with open(filepath, "wb") as f:
        pickle.dump(model, f)
    warnings.warn(
        f"Neither hummingbird-ml nor skl2onnx available — "
        f"saved as pickle to {filepath} instead of ONNX"
    )


def main() -> None:
    base = Path(__file__).resolve().parents[2]
    data_path = base / "ml" / "data" / "telemetry.parquet"

    print(f"Loading data from {data_path}")
    raw_df = pd.read_parquet(data_path)
    print(f"Loaded {len(raw_df)} rows, {len(raw_df.columns)} columns")
    print(f"Sites: {raw_df['site'].nunique()}, Devices: {raw_df['device_id'].nunique()}")

    print("Extracting features...")
    feature_matrix = extract_features(raw_df)
    print(f"Feature matrix shape: {feature_matrix.shape}")

    print("Training IsolationForest (n_estimators=200, contamination=0.05)...")
    model = train_model(feature_matrix)

    print("Running predictions...")
    predictions, scores = predict_anomaly(model, feature_matrix)

    n_anomalies = int((predictions == -1).sum())
    n_total = len(predictions)
    print(f"Anomalies detected: {n_anomalies} / {n_total} "
          f"({100.0 * n_anomalies / n_total:.2f}%)")

    checkpoint_dir = base / "ml" / "models" / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    model_path = checkpoint_dir / "isolation_forest.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved to {model_path}")

    onnx_dir = base / "ml" / "models" / "onnx"
    onnx_dir.mkdir(parents=True, exist_ok=True)
    onnx_path = onnx_dir / "isolation_forest.onnx"
    try:
        export_to_onnx(model, onnx_path)
        if onnx_path.stat().st_size > 0:
            print(f"ONNX exported to {onnx_path}")
    except Exception as exc:
        print(f"ONNX export skipped: {exc}")

    summary = get_anomaly_summary(raw_df, predictions, scores)
    print(f"\nAnomaly summary by device ({len(summary)} devices with anomalies):")
    print(summary.to_string(index=False))

    result_df = raw_df.copy()
    result_df["anomaly_score"] = scores
    result_df["is_anomaly"] = predictions == -1

    top10 = result_df[result_df["is_anomaly"]].nsmallest(10, "anomaly_score")
    print("\nTop-10 most anomalous samples (lowest anomaly scores):")
    display_cols = [c for c in [
        "timestamp", "device_id", "site", "device_role",
        "latency_ms", "packet_loss_pct", "cpu_util_pct", "anomaly_score",
    ] if c in top10.columns]
    print(top10[display_cols].to_string(index=False))


if __name__ == "__main__":
    main()
