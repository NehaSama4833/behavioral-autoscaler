import numpy as np
import sys, os
import torch
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from predictor.model import LoadPredictor

class Predictor:
    def __init__(self, weights_path="predictor/weights.pt"):
        checkpoint = torch.load(weights_path, map_location="cpu", weights_only=True)
        self.model = LoadPredictor()
        self.model.load_state_dict(checkpoint["model_state"])
        self.model.eval()
        self.feat_mean = np.array(checkpoint["feat_mean"])
        self.feat_std = np.array(checkpoint["feat_std"])

    def predict(self, signals: np.ndarray) -> float:
        normalized = (signals - self.feat_mean) / (self.feat_std + 1e-8)
        x = torch.tensor(normalized, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            return round(self.model(x).item(), 2)
