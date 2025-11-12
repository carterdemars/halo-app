from flask import Flask, request
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client(database='halo-v0')

@app.route("/", methods=["POST"])
def ingest():
    """
    Simplified HTTP ingestion endpoint for ESP32 or curl.
    Expects JSON like:
    {
        "device_id": "dog001",
        "timestamp": "2025-11-07T22:00:00Z",
        "temperature": 38.7,
        "pulse": 92,
        "respiration": 22
    }
    """
    try:
        data = request.get_json(force=True)
        required = ["device_id", "timestamp", "temperature", "pulse", "respiration"]
        if not all(k in data for k in required):
            return f"Missing required fields: {required}", 400

        device_id = data["device_id"]
        timestamp = data["timestamp"]

        # Write historical reading
        db.collection("vitals").document(device_id).collection("readings").document(timestamp).set({
            "temperature": float(data["temperature"]),
            "pulse": int(data["pulse"]),
            "respiration": int(data["respiration"]),
            "timestamp": timestamp
        })

        # Update latest snapshot
        db.collection("vitals").document(device_id).set(data, merge=True)

        print(f"[SUCCESS] Data written for {device_id} @ {timestamp}")
        return "OK", 200

    except Exception as e:
        print(f"[ERROR] {e}")
        return f"Error: {e}", 500

@app.route("/", methods=["GET"])
def health():
    return "Service is running", 200
