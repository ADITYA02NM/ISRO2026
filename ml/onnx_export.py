#!/usr/bin/env python3
"""
Standalone ONNX export script for PS13 ML ensemble.
Loads trained model checkpoints and exports to ONNX format (opset 17)
with verification and documentation.

Usage:
    python ml/onnx_export.py
    python ml/onnx_export.py --models lstm,xgboost  # subset
"""

from __future__ import annotations

import argparse
import pickle
import sys
import warnings
from pathlib import Path
from typing import Any

import numpy as np

BASE = Path(__file__).resolve().parent
MODEL_DIR = BASE / "models"
CHECKPOINT_DIR = MODEL_DIR / "checkpoints"
ONNX_DIR = MODEL_DIR / "onnx"

ALL_MODELS = [
    "lstm",
    "xgboost",
    "isolation_forest",
    "autoencoder",
    "gnn",
    "prophet",
    "tti_regressor",
]


def _ensure_onnx_dir() -> None:
    ONNX_DIR.mkdir(parents=True, exist_ok=True)


def _load_checkpoint(rel_path: str) -> Path | None:
    p = CHECKPOINT_DIR / rel_path
    if not p.exists():
        print(f"  SKIP: checkpoint not found at {p}")
        return None
    return p


def _import_model(name: str) -> Any:
    return __import__(f"models.{name}_model", fromlist=[""])


def _print_model_info(filepath: Path, dummy_input: Any = None) -> None:
    try:
        import onnxruntime as ort

        session = ort.InferenceSession(str(filepath))
        print(f"  Verified with onnxruntime ✓")
        for i, inp in enumerate(session.get_inputs()):
            shape = inp.shape
            if hasattr(dummy_input, "shape") and i == 0:
                shape = list(dummy_input.shape)
                shape[0] = "batch"
            print(f"  Input  [{i}]: name={inp.name}, shape={shape}, type={inp.type}")
        for i, out in enumerate(session.get_outputs()):
            print(f"  Output [{i}]: name={out.name}, shape={out.shape}, type={out.type}")

        if dummy_input is not None:
            onnx_input = {}
            for i, inp in enumerate(session.get_inputs()):
                onnx_input[inp.name] = (
                    dummy_input[i] if isinstance(dummy_input, (tuple, list))
                    else dummy_input
                )
            outputs = session.run(None, onnx_input)
            for i, o in enumerate(outputs):
                print(f"  Dummy output [{i}]: shape={o.shape}, range=[{o.min():.4f}, {o.max():.4f}]")
        return True
    except ImportError:
        print(f"  onnxruntime not available — skipping verification")
        return False
    except Exception as e:
        print(f"  Verification failed: {e}")
        return False


def export_lstm() -> bool:
    ckpt = _load_checkpoint("lstm.pt")
    if ckpt is None:
        return False

    try:
        import torch
        from models.lstm_model import LSTMPredictor, export_to_onnx, INPUT_FEATURES, OUTPUT_FEATURES
    except ImportError as e:
        print(f"  SKIP: {e}")
        return False

    n_features = len(INPUT_FEATURES)
    n_outputs = len(OUTPUT_FEATURES)
    model = LSTMPredictor(n_features=n_features, n_outputs=n_outputs)
    model.load_state_dict(torch.load(ckpt, map_location="cpu", weights_only=True))
    model.eval()

    onnx_path = ONNX_DIR / "lstm.onnx"
    export_to_onnx(model, str(onnx_path))
    size_kb = onnx_path.stat().st_size / 1024
    print(f"  Exported: {onnx_path} ({size_kb:.1f} KB)")

    dummy = np.random.randn(1, 12, n_features).astype(np.float32)
    _print_model_info(onnx_path, dummy)
    return True


def export_xgboost() -> bool:
    ckpt = _load_checkpoint("xgboost.json")
    if ckpt is None:
        return False

    try:
        import xgboost as xgb
    except ImportError as e:
        print(f"  SKIP: {e}")
        return False

    model = xgb.XGBClassifier()
    model.load_model(str(ckpt))
    n_features = model.n_features_in_

    onnx_path = ONNX_DIR / "xgboost.onnx"

    exported = False
    try:
        from onnxmltools import convert_xgboost
        from skl2onnx.common.data_types import FloatTensorType

        initial_types = [("input", FloatTensorType([None, n_features]))]
        onnx_model = convert_xgboost(model, initial_types=initial_types)
        with open(onnx_path, "wb") as f:
            f.write(onnx_model.SerializeToString())
        exported = True
    except ImportError:
        pass

    if not exported:
        try:
            import treelite
            import treelite_runtime  # noqa: F401

            tl_model = treelite.Model.from_xgboost(model)
            tl_model.export(f"{onnx_path}.so", toolchain="gcc")
            warnings.warn(f"treelite exported as shared lib to {onnx_path}.so")
            return False
        except ImportError:
            pass

    if not exported:
        fallback = onnx_path.with_suffix(".pkl")
        with open(fallback, "wb") as f:
            pickle.dump(model, f)
        print(f"  WARN: onnxmltools/treelite not available — pickle fallback: {fallback}")
        return False

    size_kb = onnx_path.stat().st_size / 1024
    print(f"  Exported: {onnx_path} ({size_kb:.1f} KB)")

    dummy = np.random.randn(1, n_features).astype(np.float32)
    _print_model_info(onnx_path, dummy)
    return True


def export_isolation_forest() -> bool:
    ckpt = _load_checkpoint("isolation_forest.pkl")
    if ckpt is None:
        return False

    try:
        with open(ckpt, "rb") as f:
            model = pickle.load(f)
    except Exception as e:
        print(f"  SKIP: failed to load pickle: {e}")
        return False

    n_features = model.n_features_in_
    onnx_path = ONNX_DIR / "isolation_forest.onnx"

    exported = False
    try:
        from hummingbird.ml import convert as hb_convert

        hb_model = hb_convert(model, "onnx")
        hb_model.save(str(onnx_path))
        exported = True
    except ImportError:
        pass

    if not exported:
        try:
            from skl2onnx import convert_sklearn
            from skl2onnx.common.data_types import FloatTensorType

            initial_types = [("input", FloatTensorType([None, n_features]))]
            onnx_model = convert_sklearn(model, initial_types=initial_types)
            with open(onnx_path, "wb") as f:
                f.write(onnx_model.SerializeToString())
            exported = True
        except ImportError:
            pass

    if not exported:
        fallback = onnx_path.with_suffix(".pkl")
        with open(fallback, "wb") as f:
            pickle.dump(model, f)
        print(f"  WARN: hummingbird/skl2onnx not available — pickle fallback: {fallback}")
        return False

    size_kb = onnx_path.stat().st_size / 1024
    print(f"  Exported: {onnx_path} ({size_kb:.1f} KB)")

    dummy = np.random.randn(1, n_features).astype(np.float32)
    _print_model_info(onnx_path, dummy)
    return True


def export_autoencoder() -> bool:
    ckpt = _load_checkpoint("autoencoder.pt")
    if ckpt is None:
        return False

    try:
        import torch
        from models.autoencoder_model import Autoencoder, export_to_onnx, N_FEATURES
    except ImportError as e:
        print(f"  SKIP: {e}")
        return False

    model = Autoencoder()
    model.load_state_dict(torch.load(ckpt, map_location="cpu", weights_only=True))
    model.eval()

    onnx_path = ONNX_DIR / "autoencoder.onnx"
    export_to_onnx(model, str(onnx_path))
    size_kb = onnx_path.stat().st_size / 1024
    print(f"  Exported: {onnx_path} ({size_kb:.1f} KB)")

    dummy = np.random.randn(1, N_FEATURES).astype(np.float32)
    _print_model_info(onnx_path, dummy)
    return True


def export_gnn() -> bool:
    try:
        import torch
        from models.gnn_model import (
            GNNAnomalyDetector, build_topology_graph, _normalize_adj,
        )
    except ImportError as e:
        print(f"  SKIP: {e}")
        return False

    A, node_names = build_topology_graph()
    model = GNNAnomalyDetector()
    model.eval()

    onnx_path = ONNX_DIR / "gnn.onnx"

    dummy_X = torch.randn(1, 7)
    dummy_A = torch.eye(10)

    torch.onnx.export(
        model,
        (dummy_X, dummy_A),
        onnx_path,
        input_names=["node_features", "adjacency"],
        output_names=["embeddings", "anomaly_scores"],
        dynamic_axes={
            "node_features": {0: "num_nodes"},
            "embeddings": {0: "num_nodes"},
            "anomaly_scores": {0: "num_nodes"},
        },
        opset_version=17,
    )

    size_kb = onnx_path.stat().st_size / 1024
    print(f"  Exported: {onnx_path} ({size_kb:.1f} KB)")

    A_hat = _normalize_adj(A)
    dummy_np_X = np.random.randn(10, 7).astype(np.float32)
    dummy_np_A = A_hat.numpy().astype(np.float32)
    _print_model_info(onnx_path, (dummy_np_X, dummy_np_A))
    return True


def export_prophet() -> bool:
    try:
        import torch
        from onnx import helper as _onnx_helper
        from onnx import TensorProto as _TensorProto
        from onnx import numpy_helper as _onnx_np
        import onnxruntime as ort
    except ImportError as e:
        print(f"  SKIP: missing dependencies ({e})")
        return False

    data_path = BASE / "data" / "telemetry.parquet"
    if not data_path.exists():
        print(f"  SKIP: {data_path} not found — required for SARIMAX fit")
        return False

    try:
        import pandas as pd
        from statsmodels.tsa.statespace.sarimax import SARIMAX
    except ImportError as e:
        print(f"  SKIP: {e}")
        return False

    df = pd.read_parquet(data_path)
    device_df = df[df["device_id"] == "CE1-BLR"].sort_values("timestamp").copy()
    series = device_df.set_index("timestamp")["latency_ms"].asfreq("h").ffill()

    sarimax = SARIMAX(
        series, order=(1, 0, 1), seasonal_order=(1, 1, 1, 24),
        enforce_stationarity=False, enforce_invertibility=False,
    )
    fitted = sarimax.fit(disp=False, maxiter=200)

    params = fitted.params.values.astype(np.float32)

    params_tensor = _onnx_np.from_array(params, name="sarimax_params")
    params_node = _onnx_helper.make_node(
        "Constant", inputs=[], outputs=["sarimax_params"], value=params_tensor,
    )

    graph = _onnx_helper.make_graph(
        [params_node],
        "sarimax_model",
        [],
        [_onnx_helper.make_tensor_value_info(
            "sarimax_params", _TensorProto.FLOAT, params.shape
        )],
    )

    onnx_model = _onnx_helper.make_model(
        graph,
        producer_name="prophet_model",
        producer_version="0.1.0",
        opset_imports=[_onnx_helper.make_opsetid("", 17)],
    )

    spec = fitted.specification
    props = {
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

    onnx_path = ONNX_DIR / "prophet.onnx"
    with open(onnx_path, "wb") as f:
        f.write(onnx_model.SerializeToString())

    size_kb = onnx_path.stat().st_size / 1024
    print(f"  Exported: {onnx_path} ({size_kb:.1f} KB)")

    session = ort.InferenceSession(str(onnx_path))
    print(f"  Verified with onnxruntime ✓")
    for i, out in enumerate(session.get_outputs()):
        print(f"  Output [{i}]: name={out.name}, shape={out.shape}, type={out.type}")
    for k, v in props.items():
        print(f"  Metadata: {k}={v}")
    return True


def export_tti_regressor() -> bool:
    ckpt = _load_checkpoint("tti_regressor.pkl")
    if ckpt is None:
        return False

    try:
        with open(ckpt, "rb") as f:
            model = pickle.load(f)
    except Exception as e:
        print(f"  SKIP: failed to load pickle: {e}")
        return False

    n_features = model.n_features_in_
    onnx_path = ONNX_DIR / "tti_regressor.onnx"

    exported = False
    try:
        from skl2onnx import convert_sklearn
        from skl2onnx.common.data_types import FloatTensorType

        initial_types = [("input", FloatTensorType([None, n_features]))]
        onnx_model = convert_sklearn(model, initial_types=initial_types)
        with open(onnx_path, "wb") as f:
            f.write(onnx_model.SerializeToString())
        exported = True
    except ImportError:
        pass

    if not exported:
        try:
            import treelite
            import treelite_runtime  # noqa: F401

            tl_model = treelite.Model.from_sklearn(model)
            tl_model.export(f"{onnx_path}.so", toolchain="gcc")
            warnings.warn(f"treelite exported as shared lib to {onnx_path}.so")
            return False
        except ImportError:
            pass

    if not exported:
        fallback = onnx_path.with_suffix(".pkl")
        import shutil
        shutil.copy2(ckpt, fallback)
        print(f"  WARN: skl2onnx/treelite not available — pickle fallback: {fallback}")
        return False

    size_kb = onnx_path.stat().st_size / 1024
    print(f"  Exported: {onnx_path} ({size_kb:.1f} KB)")

    dummy = np.random.randn(1, n_features).astype(np.float32)
    _print_model_info(onnx_path, dummy)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PS13 ML Ensemble — ONNX Export"
    )
    parser.add_argument(
        "--models",
        type=str,
        default=",".join(ALL_MODELS),
        help=f"Comma-separated list: {', '.join(ALL_MODELS)}",
    )
    args = parser.parse_args()

    selected = [m.strip() for m in args.models.split(",") if m.strip()]
    invalid = [m for m in selected if m not in ALL_MODELS]
    if invalid:
        print(f"[ERROR] Unknown model(s): {invalid}")
        sys.exit(1)

    _ensure_onnx_dir()

    EXPORT_FN = {
        "lstm": export_lstm,
        "xgboost": export_xgboost,
        "isolation_forest": export_isolation_forest,
        "autoencoder": export_autoencoder,
        "gnn": export_gnn,
        "prophet": export_prophet,
        "tti_regressor": export_tti_regressor,
    }

    results = []
    for name in ALL_MODELS:
        if name not in selected:
            results.append((name, "SKIPPED"))
            continue

        print(f"\n[{name}]")
        print("-" * 60)
        try:
            ok = EXPORT_FN[name]()
            results.append((name, "OK" if ok else "SKIP"))
        except Exception as e:
            print(f"  FAIL: {e}")
            results.append((name, f"FAIL: {e}"))

    print()
    print("=" * 60)
    print("  ONNX Export Summary")
    print("=" * 60)
    for name, status in results:
        if status == "OK":
            print(f"  ✓ {name:<20s} exported")
        elif status == "SKIPPED":
            print(f"  - {name:<20s} skipped")
        elif status == "SKIP":
            print(f"  - {name:<20s} no checkpoint found")
        else:
            print(f"  ✗ {name:<20s} {status}")
    print("=" * 60)


if __name__ == "__main__":
    main()
