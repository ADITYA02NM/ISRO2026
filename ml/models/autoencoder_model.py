"""
PyTorch Autoencoder for reconstruction-based anomaly detection on network telemetry.
Part of PS13 predictive SD-WAN NOC ensemble.

Learns normal network behavior patterns; flags anomalies via high reconstruction error.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset

INPUT_FEATURES = [
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

N_FEATURES = len(INPUT_FEATURES)
ENCODING_DIM = 16


class Autoencoder(nn.Module):
    def __init__(self, n_features: int = N_FEATURES) -> None:
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(n_features, 32),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(32, ENCODING_DIM),
            nn.ReLU(),
        )
        self.decoder = nn.Sequential(
            nn.Linear(ENCODING_DIM, 32),
            nn.ReLU(),
            nn.Linear(32, n_features),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.decoder(self.encoder(x))


def prepare_data(
    df: pd.DataFrame,
) -> Tuple[DataLoader, DataLoader, StandardScaler, np.ndarray, np.ndarray]:
    missing = [c for c in INPUT_FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    raw = df[INPUT_FEATURES].dropna().values.astype(np.float32)

    scaler = StandardScaler()
    normalized = scaler.fit_transform(raw).astype(np.float32)

    split = int(0.8 * len(normalized))
    X_train, X_val = normalized[:split], normalized[split:]

    train_loader = DataLoader(
        TensorDataset(torch.from_numpy(X_train)),
        batch_size=32,
        shuffle=True,
    )
    val_loader = DataLoader(
        TensorDataset(torch.from_numpy(X_val)),
        batch_size=32,
        shuffle=False,
    )
    return train_loader, val_loader, scaler, X_train, X_val


def train_model(
    train_loader: DataLoader,
    val_loader: DataLoader,
    epochs: int = 100,
    lr: float = 0.001,
    patience: int = 10,
) -> Autoencoder:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Autoencoder().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    best_val_loss = float("inf")
    patience_counter = 0
    best_state: dict[str, torch.Tensor] | None = None

    for epoch in range(1, epochs + 1):
        model.train()
        train_loss = 0.0
        for (batch,) in train_loader:
            batch = batch.to(device)
            optimizer.zero_grad()
            loss = criterion(model(batch), batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * batch.size(0)
        train_loss /= len(train_loader.dataset)

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for (batch,) in val_loader:
                batch = batch.to(device)
                loss = criterion(model(batch), batch)
                val_loss += loss.item() * batch.size(0)
        val_loss /= len(val_loader.dataset)

        if (epoch - 1) % 10 == 0 or epoch == epochs:
            print(f"Epoch {epoch:3d}/{epochs}  train_loss={train_loss:.6f}  val_loss={val_loss:.6f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = model.state_dict()
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch}")
                break

    model.load_state_dict(best_state)
    return model


@torch.no_grad()
def compute_anomaly_scores(
    model: Autoencoder,
    df: pd.DataFrame,
    scaler: StandardScaler,
) -> np.ndarray:
    device = next(model.parameters()).device
    model.eval()

    raw = df[INPUT_FEATURES].dropna().values.astype(np.float32)
    normalized = scaler.transform(raw).astype(np.float32)
    tensor = torch.from_numpy(normalized).to(device)

    reconstructed = model(tensor)
    mse = torch.mean((tensor - reconstructed) ** 2, dim=1)
    return mse.cpu().numpy()


@torch.no_grad()
def detect_anomalies(
    model: Autoencoder,
    df: pd.DataFrame,
    scaler: StandardScaler,
    threshold_percentile: float = 95,
) -> Tuple[np.ndarray, float]:
    scores = compute_anomaly_scores(model, df, scaler)
    threshold = float(np.percentile(scores, threshold_percentile))
    flags = scores > threshold
    return flags, threshold


def export_to_onnx(
    model: Autoencoder,
    filepath: str | Path,
) -> None:
    device = next(model.parameters()).device
    model.eval()
    dummy = torch.randn(1, N_FEATURES).to(device)

    torch.onnx.export(
        model,
        dummy,
        filepath,
        input_names=["input"],
        output_names=["reconstructed"],
        dynamic_axes={
            "input": {0: "batch_size"},
            "reconstructed": {0: "batch_size"},
        },
        opset_version=17,
    )


def load_synthetic_data(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    missing = [c for c in INPUT_FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in data: {missing}")
    return df.dropna().reset_index(drop=True)


def main() -> None:
    torch.manual_seed(42)
    np.random.seed(42)

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    DATA_PATH = PROJECT_ROOT / "ml" / "data" / "telemetry.parquet"
    CHECKPOINT_DIR = PROJECT_ROOT / "ml" / "models" / "checkpoints"
    ONNX_DIR = PROJECT_ROOT / "ml" / "models" / "onnx"
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    ONNX_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading data from {DATA_PATH}")
    df = load_synthetic_data(str(DATA_PATH))
    print(f"Loaded {len(df)} rows")

    train_loader, val_loader, scaler, X_train, X_val = prepare_data(df)
    print(f"Train samples: {len(X_train)}, Val samples: {len(X_val)}")

    print("Training Autoencoder...")
    model = train_model(train_loader, val_loader)

    scores = compute_anomaly_scores(model, df, scaler)
    threshold = float(np.percentile(scores, 95))
    anomaly_count = int(np.sum(scores > threshold))
    print(f"Reconstruction error 95th percentile threshold: {threshold:.6f}")
    print(f"Anomalies detected: {anomaly_count} / {len(scores)} ({100 * anomaly_count / len(scores):.1f}%)")

    checkpoint_path = CHECKPOINT_DIR / "autoencoder.pt"
    torch.save(model.state_dict(), checkpoint_path)
    print(f"Checkpoint saved to {checkpoint_path}")

    onnx_path = ONNX_DIR / "autoencoder.onnx"
    export_to_onnx(model, str(onnx_path))
    print(f"ONNX model exported to {onnx_path}")

    model.eval()
    device = next(model.parameters()).device
    criterion = nn.MSELoss()
    val_loss = 0.0
    with torch.no_grad():
        for (batch,) in val_loader:
            batch = batch.to(device)
            loss = criterion(model(batch), batch)
            val_loss += loss.item() * batch.size(0)
    val_loss /= len(val_loader.dataset)
    print(f"Final validation loss (MSE): {val_loss:.6f}")


if __name__ == "__main__":
    main()
