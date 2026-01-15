import os
import time
from joblib import load
from sklearn.metrics import f1_score
from prometheus_client import Gauge, start_http_server

MODEL_F1 = Gauge("model_f1", "F1 score on latest labeled batch")

BATCH_PATH = os.environ.get("BATCH_PATH", r".\shared\batch_for_monitoring.joblib")
PORT = int(os.environ.get("PORT", "8000"))

def main():
    start_http_server(PORT, addr="0.0.0.0")

    while True:
        if os.path.exists(BATCH_PATH):
            payload = load(BATCH_PATH)
            y_true = payload["y_true"]
            y_pred = payload["y_pred"]
            MODEL_F1.set(float(f1_score(y_true, y_pred)))
        time.sleep(15)

if __name__ == "__main__":
    main()