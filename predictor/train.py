import sys, os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from predictor.model import LoadPredictor

SEQ_LEN, EPOCHS, BATCH_SIZE, LR = 20, 30, 32, 0.001

def load_data(path="data/sample_signals.csv"):
    df = pd.read_csv(path)
    features = df[["active_players", "queue_size", "login_rate", "chat_rate"]].values
    labels = df["cpu_load"].values
    feat_mean = features.mean(axis=0)
    feat_std = features.std(axis=0) + 1e-8
    features = (features - feat_mean) / feat_std
    X, y = [], []
    for i in range(len(features) - SEQ_LEN):
        X.append(features[i:i + SEQ_LEN])
        y.append(labels[i + SEQ_LEN])
    X = torch.tensor(np.array(X), dtype=torch.float32)
    y = torch.tensor(np.array(y), dtype=torch.float32).unsqueeze(1)
    return X, y, feat_mean, feat_std

def train():
    print("Loading data...")
    X, y, feat_mean, feat_std = load_data()
    split = int(0.8 * len(X))
    train_loader = DataLoader(TensorDataset(X[:split], y[:split]), batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(TensorDataset(X[split:], y[split:]), batch_size=BATCH_SIZE)

    model = LoadPredictor()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    loss_fn = nn.MSELoss()
    train_losses, val_losses = [], []

    print(f"Training for {EPOCHS} epochs...")
    for epoch in range(EPOCHS):
        model.train()
        total = sum(
            (lambda loss: (optimizer.zero_grad(), loss.backward(), optimizer.step(), loss.item())[-1])(loss_fn(model(xb), yb))
            for xb, yb in train_loader
        )
        model.eval()
        val_total = sum(loss_fn(model(xb), yb).item() for xb, yb in val_loader)
        with torch.no_grad():
            pass
        train_losses.append(total / len(train_loader))
        val_losses.append(val_total / len(val_loader))
        print(f"  Epoch {epoch+1:02d}/{EPOCHS} — Train: {train_losses[-1]:.4f} | Val: {val_losses[-1]:.4f}")

    os.makedirs("predictor", exist_ok=True)
    torch.save({"model_state": model.state_dict(), "feat_mean": feat_mean.tolist(), "feat_std": feat_std.tolist()}, "predictor/weights.pt")
    print("\nSaved: predictor/weights.pt")

    plt.figure(figsize=(8, 4))
    plt.plot(train_losses, label="Train Loss")
    plt.plot(val_losses, label="Val Loss")
    plt.xlabel("Epoch"); plt.ylabel("MSE Loss"); plt.title("Training Progress"); plt.legend()
    plt.tight_layout(); plt.savefig("predictor/training_loss.png")
    print("Saved: predictor/training_loss.png")

if __name__ == "__main__":
    train()
