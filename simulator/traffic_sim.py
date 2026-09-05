import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

def generate_spike_data(hours=24, interval_seconds=30, spike_hour=14):
    timestamps, active_players, queue_size, login_rate, chat_rate, cpu_load = [], [], [], [], [], []
    base_time = datetime(2024, 1, 1, 0, 0, 0)
    steps = int(hours * 3600 / interval_seconds)

    for i in range(steps):
        t = base_time + timedelta(seconds=i * interval_seconds)
        hour = t.hour
        base = 100 + 80 * np.sin(np.pi * hour / 12)
        spike = 400 * np.exp(-0.5 * ((hour - spike_hour) / 0.5) ** 2)
        noise = np.random.normal(0, 10)
        players = max(0, int(base + spike + noise))

        timestamps.append(t)
        active_players.append(players)
        queue_size.append(int(players * 0.3 + np.random.normal(0, 5)))
        login_rate.append(int(players * 0.05 + np.random.normal(0, 2)))
        chat_rate.append(int(players * 0.8 + np.random.normal(0, 20)))

        lag_index = max(0, i - 20)
        lagged_players = active_players[lag_index]
        cpu_load.append(round(min(100, lagged_players / 6 + np.random.normal(0, 2)), 2))

    return pd.DataFrame({
        "timestamp": timestamps,
        "active_players": active_players,
        "queue_size": queue_size,
        "login_rate": login_rate,
        "chat_rate": chat_rate,
        "cpu_load": cpu_load
    })

if __name__ == "__main__":
    print("Generating synthetic player spike dataset...")
    os.makedirs("data", exist_ok=True)
    df = generate_spike_data()
    df.to_csv("data/sample_signals.csv", index=False)
    print(f"Done. {len(df)} rows saved to data/sample_signals.csv")
    print(df.head(5).to_string())
