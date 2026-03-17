from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency', ['endpoint'])

@app.route("/")
def index():
    start = time.time()
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    time.sleep(random.uniform(0.1, 0.5))  # simulate latency
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start)
    return jsonify({"message": "Hello from Flask!"})

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
