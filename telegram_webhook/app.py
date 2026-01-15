import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)

@app.post("/alert")
def alert():
    payload = request.get_json(force=True, silent=True) or {}
    alerts = payload.get("alerts", [])

    for a in alerts:
        status = a.get("status")
        labels = a.get("labels", {})
        ann = a.get("annotations", {})
        name = labels.get("alertname", "Alert")
        summary = ann.get("summary", "")
        description = ann.get("description", "")

        text = f"[{status}] {name}\n{summary}\n{description}\nlabels={labels}"
        send_telegram(text)

    return {"ok": True}