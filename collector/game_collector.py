import pandas as pd
import numpy as np
from datetime import datetime

class GameSignalCollector:
    """
    Reads player behavior signals into a rolling buffer.
    Reads from the sample CSV to simulate live game server data.
    In production, connect this to your game server API.
    """
    def __init__(self, seq_len=20, data_path="data/sample_signals.csv"):
        self.seq_len = seq_len
        self.df = pd.read_csv(data_path)
        self.features = self.df[["active_players", "queue_size", "login_rate", "chat_rate"]].values
        self._index = 1600

    def get_latest_signals(self):
        if self._index + self.seq_len >= len(self.features):
            self._index = 0
        signals = self.features[self._index:self._index + self.seq_len]
        self._index += 1
        return signals.astype(np.float32)

    def get_current_stats(self):
        row = self.features[self._index]
        return {
            "active_players": int(row[0]),
            "queue_size": int(row[1]),
            "login_rate": int(row[2]),
            "chat_rate": int(row[3]),
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
