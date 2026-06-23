#!/usr/bin/env python3
"""
Master training orchestrator for PS13 ML ensemble.
Trains all 7 models in dependency order with per-model toggling.

Usage:
    python ml/train_all.py                          # train all
    python ml/train_all.py --models xgboost,prophet  # train subset
    python ml/train_all.py --skip-data                # skip data generation
"""

from __future__ import annotations

import argparse
import importlib
import sys
import time
from pathlib import Path
from typing import Any, Callable

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

ALL_MODELS = [
    "xgboost",
    "isolation_forest",
    "tti_regressor",
    "prophet",
    "lstm",
    "autoencoder",
    "gnn",
]


def _import_model(name: str) -> Any:
    return importlib.import_module(f"models.{name}_model")


def _time_it(fn: Callable, label: str) -> dict[str, Any]:
    start = time.time()
    try:
        fn()
        elapsed = time.time() - start
        return {"model": label, "status": "OK", "seconds": round(elapsed, 2)}
    except Exception as e:
        elapsed = time.time() - start
        return {"model": label, "status": f"FAIL: {e}", "seconds": round(elapsed, 2)}


def train_xgboost() -> None:
    mod = _import_model("xgboost")
    print("\n" + "=" * 60)
    print("  Training XGBoost Classifier")
    print("=" * 60)
    mod.main()


def train_isolation_forest() -> None:
    mod = _import_model("isolation_forest")
    print("\n" + "=" * 60)
    print("  Training IsolationForest")
    print("=" * 60)
    mod.main()


def train_tti_regressor() -> None:
    mod = _import_model("tti_regressor")
    print("\n" + "=" * 60)
    print("  Training TTI Regressor")
    print("=" * 60)
    mod.main()


def train_prophet() -> None:
    mod = _import_model("prophet")
    print("\n" + "=" * 60)
    print("  Training Prophet / StatsModels")
    print("=" * 60)
    mod.main()


def train_lstm() -> None:
    mod = _import_model("lstm")
    print("\n" + "=" * 60)
    print("  Training LSTM (requires torch)")
    print("=" * 60)
    mod.main()


def train_autoencoder() -> None:
    mod = _import_model("autoencoder")
    print("\n" + "=" * 60)
    print("  Training Autoencoder (requires torch)")
    print("=" * 60)
    mod.main()


def train_gnn() -> None:
    mod = _import_model("gnn")
    print("\n" + "=" * 60)
    print("  Training GNN (requires torch + networkx)")
    print("=" * 60)
    mod.main()


def _print_summary(results: list[dict[str, Any]]) -> None:
    print()
    print("=" * 72)
    print("  Training Summary")
    print("=" * 72)
    print(f"  {'Model':<22s} {'Status':<35s} {'Time (s)':>10s}")
    print(f"  {'-' * 22} {'-' * 35} {'-' * 10}")
    for r in results:
        status = r["status"]
        if status.startswith("FAIL"):
            status = f"✗ {status}"
        else:
            status = f"✓ {status}"
        print(f"  {r['model']:<22s} {status:<35s} {r['seconds']:>10.2f}")
    ok = sum(1 for r in results if r["status"] == "OK")
    print(f"  {'-' * 22} {'-' * 35} {'-' * 10}")
    print(f"  {'TOTAL':<22s} {f'{ok}/{len(results)} passed':<35s} "
          f"{sum(r['seconds'] for r in results):>10.2f}")
    print("=" * 72)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PS13 ML Ensemble — Master Training Orchestrator"
    )
    parser.add_argument(
        "--models",
        type=str,
        default=",".join(ALL_MODELS),
        help=f"Comma-separated list of models to train: {', '.join(ALL_MODELS)}",
    )
    parser.add_argument(
        "--skip-data",
        action="store_true",
        help="Skip synthetic data generation (use existing)",
    )
    args = parser.parse_args()

    selected = [m.strip() for m in args.models.split(",") if m.strip()]
    invalid = [m for m in selected if m not in ALL_MODELS]
    if invalid:
        print(f"[ERROR] Unknown model(s): {invalid}")
        print(f"  Valid models: {', '.join(ALL_MODELS)}")
        sys.exit(1)

    print("=" * 72)
    print("  PS13 ML Ensemble — Master Training Orchestrator")
    print("=" * 72)

    if not args.skip_data:
        print("\n[STEP 0] Generating synthetic data...")
        try:
            from generate_synthetic_data import main as gen_data
            gen_data()
            print("[STEP 0] Data generation complete.")
        except Exception as e:
            print(f"[FATAL] Data generation failed: {e}")
            sys.exit(1)
    else:
        print("\n[STEP 0] Skipping data generation (--skip-data)")

    TRAIN_FN: dict[str, Callable] = {
        "xgboost": train_xgboost,
        "isolation_forest": train_isolation_forest,
        "tti_regressor": train_tti_regressor,
        "prophet": train_prophet,
        "lstm": train_lstm,
        "autoencoder": train_autoencoder,
        "gnn": train_gnn,
    }

    results: list[dict[str, Any]] = []
    for model_name in ALL_MODELS:
        if model_name not in selected:
            results.append({
                "model": model_name,
                "status": "SKIPPED",
                "seconds": 0.0,
            })
            continue
        result = _time_it(TRAIN_FN[model_name], model_name)
        results.append(result)
        if result["status"] != "OK":
            print(f"  ⚠ {model_name} failed, continuing with remaining models...")

    print()
    print("=" * 72)
    print("  Exporting all models to ONNX")
    print("=" * 72)
    onnx_script = BASE / "onnx_export.py"
    if onnx_script.exists():
        try:
            from onnx_export import main as export_onnx
            export_onnx()
        except Exception as e:
            print(f"[WARN] ONNX export failed: {e}")
    else:
        print(f"[WARN] {onnx_script} not found — skipping ONNX export")

    _print_summary(results)


if __name__ == "__main__":
    main()
