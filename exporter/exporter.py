import os
import time
from joblib import load
from sklearn.metrics import f1_score
from prometheus_client import Gauge, start_http_server

MODEL_F1 = Gauge("model_f1", "F1 score (switches from reference to current)")
MODEL_PHASE = Gauge("model_phase", "0=reference, 1=current")

REF_PATH = os.environ.get("REF_PATH", "/shared/reference_batch.joblib")
CUR_PATH = os.environ.get("CUR_PATH", "/shared/current_batch.joblib")
SWITCH_AFTER_SEC = int(os.environ.get("SWITCH_AFTER_SEC", "120"))
PORT = int(os.environ.get("PORT", "8000"))

def calc_f1(path: str) -> float:
    payload = load(path)
    return float(f1_score(payload["y_true"], payload["y_pred"]))

def main():
    start_http_server(PORT, addr="0.0.0.0")

    # reference
    ref_f1 = calc_f1(REF_PATH)
    MODEL_F1.set(ref_f1)
    MODEL_PHASE.set(0)
    print(f"[exporter] reference F1={ref_f1:.4f}. Switching in {SWITCH_AFTER_SEC}s...")
    time.sleep(SWITCH_AFTER_SEC)

    # current
    cur_f1 = calc_f1(CUR_PATH)
    MODEL_F1.set(cur_f1)
    MODEL_PHASE.set(1)
    print(f"[exporter] current F1={cur_f1:.4f}. Now staying on current.")

    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()