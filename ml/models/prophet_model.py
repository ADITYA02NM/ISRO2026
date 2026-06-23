"""
Prophet-style seasonal trend decomposition model for network telemetry.
Uses statsmodels as a Prophet-compatible fallback for seasonality/trend
decomposition and SARIMAX forecasting. Part of PS13 ML ensemble.
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Graceful imports — Prophet is unavailable; fall back to statsmodels
# ---------------------------------------------------------------------------
try:
    from statsmodels.tsa.seasonal import seasonal_decompose as _seasonal_decompose
    from statsmodels.tsa.statespace.sarimax import SARIMAX as _SARIMAX
    from statsmodels.stats.diagnostic import acorr_ljungbox as _ljungbox
    from statsmodels.tools.sm_exceptions import ConvergenceWarning

    _HAS_STATS = True
except ImportError:
    _seasonal_decompose = None
    _SARIMAX = None
    _ljungbox = None
    _HAS_STATS = False
    ConvergenceWarning = None

try:
    import onnx
    from onnx import helper as _onnx_helper
    from onnx import TensorProto as _TensorProto
    from onnx import numpy_helper as _onnx_np

    _HAS_ONNX = True
except ImportError:
    onnx = None
    _onnx_helper = None
    _TensorProto = None
    _onnx_np = None
    _HAS_ONNX = False

warnings.filterwarnings("ignore", category=FutureWarning)
if ConvergenceWarning is not None:
    warnings.filterwarnings("ignore", category=ConvergenceWarning)

SEED = 42


def decompose_timeseries(
    df: pd.DataFrame,
    metric: str,
    period: int = 24,
) -> dict[str, pd.Series]:
    """Decompose a metric into trend / seasonal / residual components.

    Parameters
    ----------
    df : DataFrame
        Must contain ``timestamp`` and ``{metric}`` columns.
    metric : str
        Column name to decompose (e.g. ``latency_ms``).
    period : int
        Seasonal period in time-steps (default 24 for hourly data).

    Returns
    -------
    dict[str, pd.Series]
        Keys ``trend``, ``seasonal``, ``residual``, each a time-indexed Series.
    """
    if not _HAS_STATS:
        raise ImportError("statsmodels is required for decomposition")

    series = df.set_index("timestamp")[metric].sort_index()
    series = series.asfreq("h").ffill()

    result = _seasonal_decompose(series, model="additive", period=period)

    return {
        "trend": result.trend.dropna(),
        "seasonal": result.seasonal.dropna(),
        "residual": result.resid.dropna(),
    }


def detect_anomalies(
    series: pd.Series,
    threshold: float = 3.0,
    period: int = 24,
) -> pd.DataFrame:
    """Detect anomalies using residual z-score from seasonal decomposition.

    Parameters
    ----------
    series : pd.Series
        Time-indexed metric values (e.g. ``latency_ms``).
    threshold : float
        Z-score threshold above which a point is flagged (default 3.0).
    period : int
        Seasonal period (default 24 for hourly data).

    Returns
    -------
    pd.DataFrame
        Columns ``value``, ``trend``, ``seasonal``, ``residual``, ``z_score``,
        ``is_anomaly``.  Index matches the original series index.
    """
    if not _HAS_STATS:
        raise ImportError("statsmodels is required for anomaly detection")

    freq = pd.infer_freq(series.index)
    if freq is None:
        series = series.copy()
        series.index = pd.date_range(
            start=series.index[0], periods=len(series), freq="h"
        )

    series = series.asfreq("h").ffill()

    result = _seasonal_decompose(series, model="additive", period=period)
    residual = result.resid.dropna()

    if len(residual) < 2:
        return pd.DataFrame(
            {"value": series, "is_anomaly": False},
            index=series.index,
        )

    z_scores = (residual - residual.mean()) / residual.std()
    is_anomaly = z_scores.abs() > threshold

    out = pd.DataFrame(
        {
            "value": series,
            "trend": result.trend,
            "seasonal": result.seasonal,
            "residual": residual,
            "z_score": z_scores,
            "is_anomaly": is_anomaly,
        },
        index=series.index,
    )
    out["is_anomaly"] = out["is_anomaly"].fillna(False)
    return out


def forecast(
    series: pd.Series,
    steps: int = 24,
    seasonal_order: tuple[int, int, int, int] = (1, 1, 1, 24),
) -> dict[str, np.ndarray | pd.DatetimeIndex]:
    """SARIMAX forecast for the next *steps* time-steps.

    Parameters
    ----------
    series : pd.Series
        Time-indexed historical values.
    steps : int
        Number of steps ahead to forecast (default 24).
    seasonal_order : tuple
        (P, D, Q, s) seasonal order (default (1,1,1,24)).

    Returns
    -------
    dict with keys ``forecast``, ``conf_int_lower``, ``conf_int_upper``,
    ``index`` (pd.DatetimeIndex of forecast horizon).
    """
    if not _HAS_STATS:
        raise ImportError("statsmodels is required for forecasting")

    freq = pd.infer_freq(series.index)
    if freq is None:
        series = series.copy()
        series.index = pd.date_range(
            start=series.index[0], periods=len(series), freq="h"
        )

    series = series.asfreq("h").ffill()

    model = _SARIMAX(
        series,
        order=(1, 0, 1),
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    fitted = model.fit(disp=False, maxiter=200)

    result = fitted.get_forecast(steps=steps)
    pred = result.predicted_mean
    ci = result.conf_int(alpha=0.05)

    forecast_index = pd.date_range(
        start=series.index[-1] + pd.Timedelta(hours=1),
        periods=steps,
        freq="h",
    )

    return {
        "forecast": pred.values,
        "conf_int_lower": ci.iloc[:, 0].values if isinstance(ci, pd.DataFrame) else ci[:, 0],
        "conf_int_upper": ci.iloc[:, 1].values if isinstance(ci, pd.DataFrame) else ci[:, 1],
        "index": forecast_index,
    }


def compute_anomaly_score(
    series: pd.Series,
    period: int = 24,
) -> float:
    """Compute a normalised anomaly score (0-1) based on residual magnitude.

    Uses the 95th percentile of the absolute residual z-score, capped at 5,
    then divided by 5 to map into [0, 1].

    Parameters
    ----------
    series : pd.Series
        Time-indexed metric values.
    period : int
        Seasonal period (default 24).

    Returns
    -------
    float
        Anomaly score in [0, 1].  0 = normal, 1 = highly anomalous.
    """
    if not _HAS_STATS:
        raise ImportError("statsmodels is required for anomaly scoring")

    freq = pd.infer_freq(series.index)
    if freq is None:
        series = series.copy()
        series.index = pd.date_range(
            start=series.index[0], periods=len(series), freq="h"
        )

    series = series.asfreq("h").ffill()

    result = _seasonal_decompose(series, model="additive", period=period)
    residual = result.resid.dropna()

    if len(residual) < 2 or residual.std() == 0:
        return 0.0

    z_scores = (residual - residual.mean()).abs() / residual.std()
    p95 = float(np.percentile(z_scores, 95))
    score = min(1.0, p95 / 5.0)
    return round(score, 4)


def residual_diagnostics(
    residual: pd.Series,
    lags: list[int] | None = None,
) -> dict[str, Any]:
    """Run Ljung-Box test on residuals to check for remaining autocorrelation.

    Parameters
    ----------
    residual : pd.Series
        Residuals from decomposition or model fit.
    lags : list[int] | None
        Lags to test (default ``[24]``).

    Returns
    -------
    dict with keys ``lb_stat``, ``lb_pvalue``, ``is_white_noise``.
    """
    if not _HAS_STATS:
        raise ImportError("statsmodels is required for residual diagnostics")

    if lags is None:
        lags = [24]

    resid = residual.dropna()
    if len(resid) < max(lags) + 1:
        return {"lb_stat": np.nan, "lb_pvalue": np.nan, "is_white_noise": True}

    lb = _ljungbox(resid, lags=lags, return_df=True)
    lb_stat = lb["lb_stat"].values
    lb_pvalue = lb["lb_pvalue"].values

    return {
        "lb_stat": lb_stat,
        "lb_pvalue": lb_pvalue,
        "is_white_noise": bool(np.all(lb_pvalue > 0.05)),
    }


def export_to_onnx(
    model: Any,
    filepath: str | Path,
) -> None:
    """Export SARIMAX model parameters as a simple ONNX constant graph.

    Stores fitted coefficients and model-structure metadata in ONNX format
    for inference portability.

    Parameters
    ----------
    model : SARIMAXResultsWrapper
        A fitted SARIMAX model result.
    filepath : str | Path
        Destination path for the ``.onnx`` file.

    Raises
    ------
    ImportError
        If ``onnx`` package is not installed.
    TypeError
        If *model* is not a fitted SARIMAX result.
    """
    if not _HAS_ONNX:
        raise ImportError(
            "ONNX export requires the 'onnx' package. "
            "Install with: pip install onnx"
        )
    if not _HAS_STATS:
        raise ImportError("statsmodels is required to export SARIMAX model")

    from statsmodels.tsa.statespace.sarimax import SARIMAXResultsWrapper

    if not isinstance(model, SARIMAXResultsWrapper):
        raise TypeError("Expected a fitted statsmodels SARIMAXResultsWrapper")

    params = model.params.values.astype(np.float32)
    spec = model.specification

    params_tensor = _onnx_np.from_array(params, name="sarimax_params")
    params_node = _onnx_helper.make_node(
        "Constant",
        inputs=[],
        outputs=["sarimax_params"],
        value=params_tensor,
    )

    graph = _onnx_helper.make_graph(
        [params_node],
        "sarimax_model",
        [],
        [
            _onnx_helper.make_tensor_value_info(
                "sarimax_params", _TensorProto.FLOAT, params.shape
            )
        ],
    )

    onnx_model = _onnx_helper.make_model(
        graph,
        producer_name="prophet_model",
        producer_version="0.1.0",
        opset_imports=[_onnx_helper.make_opsetid("", 17)],
    )

    props: dict[str, str] = {
        "ar_order": str(spec.order[0]),
        "ma_order": str(spec.order[1]),
        "integrated_order": str(spec.order[2]),
        "seasonal_ar_order": str(spec.seasonal_order[0]),
        "seasonal_ma_order": str(spec.seasonal_order[1]),
        "seasonal_integrated_order": str(spec.seasonal_order[2]),
        "seasonal_period": str(spec.seasonal_order[3]),
        "k_exog": str(spec.k_exog),
        "k_params": str(len(params)),
    }
    for key, value in props.items():
        prop = onnx_model.metadata_props.add()
        prop.key = key
        prop.value = value

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(onnx_model.SerializeToString())


def main() -> None:
    if not _HAS_STATS:
        print("[ERROR] statsmodels is not installed — cannot run prophet_model")
        return

    np.random.seed(SEED)

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    DATA_PATH = PROJECT_ROOT / "ml" / "data" / "telemetry.parquet"
    ONNX_DIR = PROJECT_ROOT / "ml" / "models" / "onnx"
    ONNX_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_PATH.exists():
        print(f"[ERROR] Data file not found at {DATA_PATH}")
        return

    print(f"[INFO] Loading data from {DATA_PATH}")
    df = pd.read_parquet(DATA_PATH)
    print(f"[INFO] Loaded {len(df)} rows, {len(df.columns)} columns")

    device_id = "CE1-BLR"
    device_df = df[df["device_id"] == device_id].sort_values("timestamp").copy()
    print(f"[INFO] Device '{device_id}': {len(device_df)} samples")

    metric = "latency_ms"
    series = device_df.set_index("timestamp")[metric].asfreq("h").ffill()
    print(f"[INFO] Decomposing '{metric}' (period=24, n={len(series)})...")

    components = decompose_timeseries(device_df, metric, period=24)

    print(f"[INFO] Trend:      {len(components['trend'])} non-NaN points")
    print(f"[INFO] Seasonal:   {len(components['seasonal'])} non-NaN points")
    print(f"[INFO] Residual:   {len(components['residual'])} non-NaN points")

    diag = residual_diagnostics(components["residual"])
    lb_val = (
        f"{float(diag['lb_pvalue'][0]):.6f}"
        if isinstance(diag["lb_pvalue"], np.ndarray)
        else str(diag["lb_pvalue"])
    )
    print(
        f"[INFO] Ljung-Box p-value (lag=24): {lb_val}  "
        f"(white noise: {diag['is_white_noise']})"
    )

    print("\n" + "=" * 60)
    print("  Anomaly Detection")
    print("=" * 60)
    anomaly_result = detect_anomalies(series, threshold=3.0, period=24)
    anomaly_timestamps = anomaly_result.index[
        anomaly_result["is_anomaly"]
    ].tolist()
    print(f"  Anomalies detected: {len(anomaly_timestamps)}")
    if anomaly_timestamps:
        for ts in anomaly_timestamps:
            row = anomaly_result.loc[ts]
            print(
                f"    {ts}  |  value={row['value']:.4f}  "
                f"z_score={row['z_score']:.2f}"
            )
    else:
        print("  (none)")

    anomaly_score = compute_anomaly_score(series, period=24)
    print(f"  Anomaly score (0-1): {anomaly_score:.4f}")

    print("\n" + "=" * 60)
    print("  Forecast — Next 24 Hours")
    print("=" * 60)
    fc = forecast(series, steps=24, seasonal_order=(1, 1, 1, 24))
    for i in range(len(fc["index"])):
        ts = fc["index"][i]
        val = fc["forecast"][i]
        lo = fc["conf_int_lower"][i]
        hi = fc["conf_int_upper"][i]
        print(f"  {ts:%Y-%m-%d %H:00}  |  {val:.4f}  [{lo:.4f}, {hi:.4f}]")

    sarimax_model = _SARIMAX(
        series,
        order=(1, 0, 1),
        seasonal_order=(1, 1, 1, 24),
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    fitted = sarimax_model.fit(disp=False, maxiter=200)
    onnx_path = ONNX_DIR / "prophet.onnx"
    try:
        export_to_onnx(fitted, str(onnx_path))
        print(f"\n[INFO] ONNX model saved to {onnx_path}")
    except (ImportError, TypeError) as e:
        print(f"\n[WARN] ONNX export skipped: {e}")

    print("\n[DONE] Prophet-style analysis complete.")


if __name__ == "__main__":
    main()
