from flask import Flask, jsonify
import os
import socket
import logging

app = Flask(__name__)

# logowanie do stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

INSTANCE = os.getenv("INSTANCE_NAME", "Unknown")

@app.route("/")
def index():
    logging.info(f"Request served by {INSTANCE}")
    return jsonify({
        "message": f"Hello from {INSTANCE}!",
        "hostname": socket.gethostname()
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "instance": INSTANCE})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
