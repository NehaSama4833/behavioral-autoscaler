import sys, os, numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collector.game_collector import GameSignalCollector

def test_signal_shape():
    c = GameSignalCollector()
    assert c.get_latest_signals().shape == (20, 4)
    print("PASS: signal shape (20,4)")

def test_signal_dtype():
    c = GameSignalCollector()
    assert c.get_latest_signals().dtype == np.float32
    print("PASS: dtype float32")

def test_stats_keys():
    c = GameSignalCollector()
    stats = c.get_current_stats()
    for k in ["active_players","queue_size","login_rate","chat_rate","timestamp"]:
        assert k in stats
    print("PASS: stats keys correct")

if __name__ == "__main__":
    test_signal_shape(); test_signal_dtype(); test_stats_keys()
    print("\nAll collector tests passed.")
