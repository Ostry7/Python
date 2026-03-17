# Reverse Proxy + Load Balancer (Nginx + Flask)

## Overview
This project demonstrates a simple load-balanced architecture using **Nginx** as a reverse proxy for two Flask backend instances.


---

## Example Flask App (backend/app.py)

```python
from flask import Flask, jsonify
import os
import socket
import logging

app = Flask(__name__)
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

```
---

## Example nginx configuration (nginx/nginx.conf)

```conf
events { }

http {
    upstream flask_backend {
        server backend1:5000;
        server backend2:5000;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://flask_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /health {
            return 200 'OK';
            add_header Content-Type text/plain;
        }
    }
}


```

## Usage


### 1. Build and start the containers:

```bash
docker compose up --build -d
```

### 2. Test loadbalancing:
- curl localhost:8080
- curl localhost:8080
- curl localhost:8080
Should see alternating responses:
```json
{"message":"Hello from Backend-1!","hostname":"flask-app-1"}
{"message":"Hello from Backend-2!","hostname":"flask-app-2"}

```
### Health check:
```
curl localhost:8080/health
```
Output:
```json
{"status":"ok"}
```
---

## Stop & Cleanup

```bash
docker compose down -v
```

---
