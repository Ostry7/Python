# Project 9 — Monitoring Stack (Prometheus + Grafana + cAdvisor)

## Overview
This project builds a **container monitoring stack** using:
- **Prometheus** – collects and stores metrics  
- **Grafana** – visualizes metrics in dashboards  
- **cAdvisor** – exposes container-level metrics (CPU, memory, network, I/O)  
- **Flask app** – exposes custom application metrics for Prometheus  

---

---

## Example Flask Application (`backend/app.py`)
A simple Flask app that exposes a `/metrics` endpoint compatible with Prometheus.

```python
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
```

---


## Example Prometheus Configuration (`prometheus/prometheus.yml`)
```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['prometheus:9090']

  - job_name: 'flask-app'
    static_configs:
      - targets: ['flask-app:5000']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```

---


## Build and start the containers:
```bash
docker compose up --build
```

---

## Testing

### Check Prometheus
Visit [http://localhost:9090](http://localhost:9090)

- Run query: `up`
- You should see:
  ```
  up{job="prometheus"} = 1
  up{job="flask-app"} = 1
  up{job="cadvisor"} = 1
  ```

### Test Flask app
Visit [http://localhost:5000/](http://localhost:5000) several times.  
Then check [http://localhost:5000/metrics](http://localhost:5000/metrics)

Prometheus should now collect metrics like:
```
app_requests_total{method="GET",endpoint="/"} 10
```

### View cAdvisor
Visit [http://localhost:8080](http://localhost:8080)  
→ Container metrics dashboard (CPU, memory, network)

### View Grafana
Visit [http://localhost:3000](http://localhost:3000)
- Default login: `admin / admin`
- Add **Prometheus** data source (`http://prometheus:9090`)
- Import example dashboard: ID `893`

---

## Example Queries
- Total requests to Flask app:
  ```
  app_requests_total
  ```
- Average request latency:
  ```
  rate(app_request_latency_seconds_sum[1m]) / rate(app_request_latency_seconds_count[1m])
  ```
- CPU usage of containers:
  ```
  rate(container_cpu_usage_seconds_total[1m])
  ```
---
