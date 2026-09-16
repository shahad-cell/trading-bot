"""
مستقبل تنبيهات تريدنق فيو (Webhook Listener).

طريقة العمل:
1. تسوي مؤشر/استراتيجية بـ Pine Script في تريدنق فيو.
2. تسوي Alert وتحط في خانة Webhook URL رابط هذا السيرفر (يحتاج يكون
   عام/متاح على الإنترنت — محلياً تقدر تستخدم أداة مثل ngrok للتجربة).
3. أول ما الشرط يتحقق، تريدنق فيو يرسل POST request فيه رسالة التنبيه،
   وهذا السيرفر يستقبلها ويخزنها في data/tradingview_alerts.json

⚠️ هذا فقط "يستقبل ويسجل" — لا ينفذ أي أمر تداول أبداً.

التشغيل:
    python alerts/webhook_listener.py
    (يشتغل على http://localhost:5000/tradingview-alert)
"""

import json
import os
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

ALERTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "data", "tradingview_alerts.json"
)


def load_alerts() -> list:
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_alert(alert: dict) -> None:
    alerts = load_alerts()
    alerts.append(alert)
    os.makedirs(os.path.dirname(ALERTS_FILE), exist_ok=True)
    with open(ALERTS_FILE, "w", encoding="utf-8") as f:
        json.dump(alerts, f, ensure_ascii=False, indent=2)


@app.route("/tradingview-alert", methods=["POST"])
def receive_alert():
    """
    يستقبل رسالة التنبيه من تريدنق فيو.
    تريدنق فيو يرسل نص عادي أو JSON حسب إعدادك في الـ Alert.
    """
    try:
        # نحاول نقرأها كـ JSON، وإذا فشل ناخذها كنص خام
        if request.is_json:
            payload = request.get_json()
        else:
            payload = {"raw_message": request.get_data(as_text=True)}

        alert_record = {
            "received_at": datetime.now().isoformat(timespec="seconds"),
            "payload": payload,
        }

        save_alert(alert_record)
        print(f"🔔 تنبيه جديد من تريدنق فيو: {payload}")

        return jsonify({"status": "received"}), 200

    except Exception as e:
        print(f"⚠️ خطأ في معالجة التنبيه: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/health", methods=["GET"])
def health_check():
    """للتأكد إن السيرفر شغال — افتحها بالمتصفح: /health"""
    return jsonify({"status": "ok", "message": "السيرفر شغال ويستنى تنبيهات"}), 200


if __name__ == "__main__":
    print("🚀 مستقبل تنبيهات تريدنق فيو شغال على المنفذ 5000")
    print("   رابط الاستقبال: http://localhost:5000/tradingview-alert")
    print("   (للربط الفعلي مع تريدنق فيو، تحتاج رابط عام — جرّب ngrok)")
    app.run(host="0.0.0.0", port=5000, debug=False)
