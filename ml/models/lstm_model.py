import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, Optional


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

OUTPUT_FEATURES = [
    "latency_ms",
    "packet_loss_pct",
    "cpu_util_pct",
    "interface_bandwidth_util_pct",
]

SEQ_LENGTH = 12
PRED_STEPS = 3


class LSTMPredictor(nn.Module):
    def __init__(self, n_features: int, n_outputs: int, hidden_sizes: Tuple[int, int] = (128, 64)):
        super().__init__()
        self.lstm1 = nn.LSTM(
            input_size=n_features,
            hidden_size=hidden_sizes[0],
            num_layers=1,
            batch_first=True,
            dropout=0.0,
        )
        self.drop1 = nn.Dropout(0.2)
        self.lstm2 = nn.LSTM(
            input_size=hidden_sizes[0],
            hidden_size=hidden_sizes[1],
            num_layers=1,
            batch_first=True,
            dropout=0.0,
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
        return out.view(-1, PRED_STEPS, len(OUTPUT_FEATURES))


def prepare_sequences(
    df: pd.DataFrame,
    seq_length: int = SEQ_LENGTH,
    pred_steps: int = PRED_STEPS,
) -> Tuple[np.ndarray, np.ndarray]:
    data = df[INPUT_FEATURES].values.astype(np.float32)
    targets = df[OUTPUT_FEATURES].values.astype(np.float32)

    X, y = [], []
    for i in range(len(data) - seq_length - pred_steps + 1):
        X.append(data[i : i + seq_length])
        y.append(targets[i + seq_length : i + seq_length + pred_steps])

    return np.array(X), np.array(y)


def train_model(
    train_loader: DataLoader,
    val_loader: DataLoader,
    epochs: int = 100,
    lr: float = 0.001,
    patience: int = 10,
) -> LSTMPredictor:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    n_features = len(INPUT_FEATURES)
    n_outputs = len(OUTPUT_FEATURES)

    model = LSTMPredictor(n_features, n_outputs).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    best_val_loss = float("inf")
    patience_counter = 0
    best_state = None

    for epoch in range(1, epochs + 1):
        model.train()
        train_loss = 0.0
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            loss = criterion(model(X_batch), y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * X_batch.size(0)

        train_loss /= len(train_loader.dataset)

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                loss = criterion(model(X_batch), y_batch)
                val_loss += loss.item() * X_batch.size(0)

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
def predict(model: LSTMPredictor, input_seq: np.ndarray) -> np.ndarray:
    device = next(model.parameters()).device
    model.eval()
    tensor = torch.from_numpy(input_seq).float().unsqueeze(0).to(device)
    output = model(tensor)
    return output.cpu().numpy().squeeze(0)


def export_to_onnx(model: LSTMPredictor, filepath: str) -> None:
    device = next(model.parameters()).device
    model.eval()
    dummy = torch.randn(1, SEQ_LENGTH, len(INPUT_FEATURES)).to(device)

    torch.onnx.export(
        model,
        dummy,
        filepath,
        input_names=["input_seq"],
        output_names=["prediction"],
        dynamic_axes={
            "input_seq": {0: "batch_size", 1: "seq_length"},
            "prediction": {0: "batch_size"},
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

    print(f"Preparing sequences (seq_length={SEQ_LENGTH}, pred_steps={PRED_STEPS})")
    X, y = prepare_sequences(df)
    print(f"Generated {len(X)} samples. X shape: {X.shape}, y shape: {y.shape}")

    split = int(0.8 * len(X))
    X_train, X_val = X[:split], X[split:]
    y_train, y_val = y[:split], y[split:]

    train_dataset = TensorDataset(
        torch.from_numpy(X_train).float(), torch.from_numpy(y_train).float()
    )
    val_dataset = TensorDataset(
        torch.from_numpy(X_val).float(), torch.from_numpy(y_val).float()
    )
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)

    print("Training LSTM model...")
    model = train_model(train_loader, val_loader)

    checkpoint_path = CHECKPOINT_DIR / "lstm.pt"
    torch.save(model.state_dict(), checkpoint_path)
    print(f"Checkpoint saved to {checkpoint_path}")

    onnx_path = ONNX_DIR / "lstm.onnx"
    export_to_onnx(model, str(onnx_path))
    print(f"ONNX model exported to {onnx_path}")

    model.eval()
    device = next(model.parameters()).device
    criterion = nn.MSELoss()
    val_loss = 0.0
    with torch.no_grad():
        for X_batch, y_batch in val_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            loss = criterion(model(X_batch), y_batch)
            val_loss += loss.item() * X_batch.size(0)
    val_loss /= len(val_loader.dataset)
    print(f"Final validation loss (MSE): {val_loss:.6f}")


if __name__ == "__main__":
    main()
