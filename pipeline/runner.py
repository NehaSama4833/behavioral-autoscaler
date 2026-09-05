import sys, os, time, yaml
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collector.game_collector import GameSignalCollector
from predictor.predict import Predictor
from scaler.k8s_scaler import decide_replicas, scale_deployment

def load_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def run():
    print("=" * 52)
    print("   Behavioral Autoscaler — Starting")
    print("=" * 52)
    config = load_config()
    collector = GameSignalCollector()
    predictor = Predictor(weights_path=config["predictor"]["weights_path"])
    dry_run   = config["scaler"]["dry_run"]
    deploy    = config["scaler"]["deployment_name"]
    namespace = config["scaler"]["namespace"]
    interval  = config["scaler"]["interval_seconds"]
    print(f"  Mode    : {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"  Target  : {deploy} / {namespace}")
    print(f"  Interval: {interval}s\n")

    while True:
        signals  = collector.get_latest_signals()
        stats    = collector.get_current_stats()
        pred_cpu = predictor.predict(signals)
        replicas = decide_replicas(pred_cpu, config)
        print(f"[{stats['timestamp']}] Players:{stats['active_players']} Queue:{stats['queue_size']} Logins:{stats['login_rate']} Chat:{stats['chat_rate']}")
        print(f"  Predicted CPU in ~10min: {pred_cpu:.2f}%")
        scale_deployment(deploy, namespace, replicas, dry_run=dry_run)
        print()
        time.sleep(interval)

if __name__ == "__main__":
    run()
