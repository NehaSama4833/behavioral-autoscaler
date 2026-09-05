import torch
import torch.nn as nn

class LoadPredictor(nn.Module):
    """
    LSTM that takes last seq_len readings of player behavior
    and predicts CPU load 10 minutes into the future.
    Input:  (batch, seq_len, 4)
    Output: (batch, 1)
    """
    def __init__(self, input_size=4, hidden_size=64, num_layers=2, dropout=0.2):
        super(LoadPredictor, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers,
                            batch_first=True, dropout=dropout)
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])
