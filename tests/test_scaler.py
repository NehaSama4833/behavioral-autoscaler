import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scaler.k8s_scaler import decide_replicas

cfg = {"thresholds":{"high":80,"medium":60,"low":40},"replicas":{"high":10,"medium":6,"low":3,"min":1}}

def test_high():   assert decide_replicas(90, cfg) == 10;  print("PASS: 90% → 10 replicas")
def test_medium(): assert decide_replicas(70, cfg) == 6;   print("PASS: 70% → 6 replicas")
def test_low():    assert decide_replicas(50, cfg) == 3;   print("PASS: 50% → 3 replicas")
def test_idle():   assert decide_replicas(20, cfg) == 1;   print("PASS: 20% → 1 replica")

if __name__ == "__main__":
    test_high(); test_medium(); test_low(); test_idle()
    print("\nAll scaler tests passed.")
