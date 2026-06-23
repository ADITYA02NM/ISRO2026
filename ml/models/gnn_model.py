import torch
import torch.nn as nn
import torch.optim as optim
import networkx as nx
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, List, Dict


NODE_NAMES = [
    "PE1-BLR", "P1-BLR", "PE1-MUM", "P1-MUM", "PE1-CHE",
    "PE1-DEL", "P1-DEL", "CE1-BLR", "CE1-MUM", "CE1-CHE",
]

EDGES = [
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


def build_topology_graph() -> Tuple[torch.Tensor, List[str]]:
    G = nx.Graph()
    G.add_nodes_from(NODE_NAMES)
    G.add_edges_from(EDGES)
    A = nx.to_numpy_array(G, nodelist=NODE_NAMES, dtype=np.float32)
    return torch.from_numpy(A), NODE_NAMES


def extract_node_features(df: pd.DataFrame, timestamp: str) -> torch.Tensor:
    row = df[df["timestamp"] == timestamp].iloc[0]
    features = torch.zeros(len(NODE_NAMES), 7, dtype=torch.float32)
    for i, node in enumerate(NODE_NAMES):
        features[i] = torch.tensor([
            row.get(f"{node}_latency", 0.0),
            row.get(f"{node}_packet_loss", 0.0),
            row.get(f"{node}_cpu", 0.0),
            row.get(f"{node}_bandwidth", 0.0),
            row.get(f"{node}_bgp_prefix", 0.0),
            row.get(f"{node}_mpls_depth", 0.0),
            row.get(f"{node}_tcp_retrans", 0.0),
        ], dtype=torch.float32)
    return features


class GCNLayer(nn.Module):
    def __init__(self, in_dim: int, out_dim: int):
        super().__init__()
        self.W = nn.Parameter(torch.empty(in_dim, out_dim))
        nn.init.xavier_uniform_(self.W)

    def forward(self, X: torch.Tensor, A_hat: torch.Tensor) -> torch.Tensor:
        return A_hat @ X @ self.W


class GCNEncoder(nn.Module):
    def __init__(self, in_dim: int = 7, hidden_dim: int = 16, out_dim: int = 8):
        super().__init__()
        self.conv1 = GCNLayer(in_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.1)
        self.conv2 = GCNLayer(hidden_dim, out_dim)

    def forward(self, X: torch.Tensor, A_hat: torch.Tensor) -> torch.Tensor:
        h = self.conv1(X, A_hat)
        h = self.relu(h)
        h = self.dropout(h)
        h = self.conv2(h, A_hat)
        return h


class AnomalyScorer(nn.Module):
    def __init__(self, embed_dim: int = 8):
        super().__init__()
        self.fc = nn.Linear(embed_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, Z: torch.Tensor) -> torch.Tensor:
        return self.sigmoid(self.fc(Z)).squeeze(-1)


class GNNAnomalyDetector(nn.Module):
    def __init__(self, in_dim: int = 7, hidden_dim: int = 16, embed_dim: int = 8):
        super().__init__()
        self.encoder = GCNEncoder(in_dim, hidden_dim, embed_dim)
        self.scorer = AnomalyScorer(embed_dim)

    def forward(self, X: torch.Tensor, A_hat: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        Z = self.encoder(X, A_hat)
        scores = self.scorer(Z)
        return Z, scores


def _normalize_adj(A: torch.Tensor) -> torch.Tensor:
    A_aug = A + torch.eye(A.size(0), dtype=A.dtype, device=A.device)
    D = A_aug.sum(dim=1)
    D_inv_sqrt = torch.diag(D.pow(-0.5))
    return D_inv_sqrt @ A_aug @ D_inv_sqrt


def train_model(
    model: GNNAnomalyDetector,
    optimizer: optim.Optimizer,
    features: torch.Tensor,
    A: torch.Tensor,
    epochs: int = 100,
) -> List[float]:
    A_hat = _normalize_adj(A)
    A = A.to(features.device)
    criterion = nn.MSELoss()
    history = []

    for epoch in range(1, epochs + 1):
        model.train()
        optimizer.zero_grad()
        Z, _ = model(features, A_hat)
        A_pred = torch.sigmoid(Z @ Z.T)
        loss = criterion(A_pred, A)
        loss.backward()
        optimizer.step()
        history.append(loss.item())

        if (epoch - 1) % 10 == 0 or epoch == epochs:
            print(f"Epoch {epoch:3d}/{epochs}  loss={loss.item():.6f}")

    return history


@torch.no_grad()
def detect_anomalies(
    model: GNNAnomalyDetector,
    features: torch.Tensor,
    A: torch.Tensor,
) -> Dict[str, float]:
    model.eval()
    A_hat = _normalize_adj(A).to(features.device)
    _, scores = model(features, A_hat)
    return {NODE_NAMES[i]: float(scores[i].cpu()) for i in range(len(NODE_NAMES))}


def export_to_onnx(model: GNNAnomalyDetector, filepath: str) -> None:
    model.eval()
    dummy_X = torch.randn(10, 7)
    dummy_A = _normalize_adj(torch.eye(10))

    torch.onnx.export(
        model.encoder,
        (dummy_X, dummy_A),
        filepath,
        input_names=["node_features", "adjacency"],
        output_names=["embeddings"],
        dynamic_axes={
            "node_features": {0: "num_nodes"},
        },
        opset_version=17,
    )


def main() -> None:
    torch.manual_seed(42)
    np.random.seed(42)

    print("Building topology graph...")
    A, nodes = build_topology_graph()
    print(f"Adjacency matrix shape: {A.shape}, {len(nodes)} nodes")

    X = torch.rand(10, 7, dtype=torch.float32)

    model = GNNAnomalyDetector()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    print("\nTraining GNN (link prediction task)...")
    train_model(model, optimizer, X, A, epochs=100)

    print("\nRunning anomaly detection...")
    scores = detect_anomalies(model, X, A)

    print(f"\n{'Node':<12} {'Anomaly Score':<15}")
    print("-" * 27)
    for node in nodes:
        print(f"{node:<12} {scores[node]:<15.6f}")

    PROJ_ROOT = Path(__file__).resolve().parents[2]
    checkpoints_dir = PROJ_ROOT / "ml" / "models" / "checkpoints"
    checkpoints_dir.mkdir(parents=True, exist_ok=True)

    # Save PyTorch state_dict for ensemble_predictor loading
    pt_path = checkpoints_dir / "gnn.pt"
    torch.save(model.state_dict(), pt_path)
    print(f"\nCheckpoint saved to {pt_path}")

    # Export to ONNX
    onnx_dir = PROJ_ROOT / "ml" / "models" / "onnx"
    onnx_dir.mkdir(parents=True, exist_ok=True)
    onnx_path = onnx_dir / "gnn.onnx"
    export_to_onnx(model, str(onnx_path))
    print(f"ONNX model exported to {onnx_path}")


if __name__ == "__main__":
    main()
