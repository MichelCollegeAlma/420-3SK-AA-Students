from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.get("/api/health")
def health():
    return {"status":"ok"}

@app.get("/api/time")
def current_time():
    return {"now": datetime.utcnow().isoformat()+"Z"}

@app.post("/api/echo")
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"you_sent": data}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
