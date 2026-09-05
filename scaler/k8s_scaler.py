import yaml

def load_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def decide_replicas(predicted_cpu, config):
    t, r = config["thresholds"], config["replicas"]
    if predicted_cpu > t["high"]:   return r["high"]
    elif predicted_cpu > t["medium"]: return r["medium"]
    elif predicted_cpu > t["low"]:    return r["low"]
    else:                             return r["min"]

def scale_deployment(deployment_name, namespace, replicas, dry_run=True):
    if dry_run:
        print(f"  [DRY RUN] '{deployment_name}' → {replicas} replicas")
        return True
    try:
        from kubernetes import client, config as k8s_config
        k8s_config.load_kube_config()
        apps_v1 = client.AppsV1Api()
        apps_v1.patch_namespaced_deployment_scale(
            name=deployment_name, namespace=namespace,
            body={"spec": {"replicas": replicas}}
        )
        print(f"  Scaled '{deployment_name}' to {replicas} replicas")
        return True
    except Exception as e:
        print(f"  Scaling failed: {e}")
        return False
