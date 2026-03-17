# Mini ELK [Elasticsearch, Logstash, Kibana] stack

## Overview
This project demonstrates a minimal **ELK stack (Elasticsearch, Logstash, Kibana)** setup combined with a simple **Flask** application that generates logs.  
The logs are collected by **Logstash**, stored in **Elasticsearch**, and visualized in **Kibana**.

---

## Example Flask App (backend/app.py)

```python
from flask import Flask, request
import logging
import time

app = Flask(__name__)

# konfiguracja logowania do pliku
logging.basicConfig(
    filename='/var/log/app-flask.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

@app.route("/login", methods=["POST"])
def login():
    user = request.json.get("user")
    logging.info(f"User {user} logged in")
    return {"status": "ok"}

@app.route("/error")
def error():
    try:
        1 / 0
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
```
---

## Example Logstash configuration (logstash/logstash.conf)

```conf
input {
  file {
    path => "/var/logs/app-flask.log"
    start_position => "beginning"
    sincedb_path => "/dev/null" 
  }
}

filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:msg}" }
  }
  date {
    match => [ "timestamp", "ISO8601" ]
  }
}

output {
  stdout { codec => rubydebug }  # do testów
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "flask-logs-%{+YYYY.MM.dd}"
  }
}

```

## Usage


### 1. Build and start the containers:

```bash
docker compose up --build -d
```

### 2. Access the services:
Once started:
- Flask app → http://localhost:8001
- Kibana → http://localhost:5601
- Elasticsearch → http://localhost:9200
---

## Test log generation
Run the following commands to generate logs from the Flask app:
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"user":"John"}' http://localhost:8001/login

curl http://localhost:8001/error
```
## Verify in Kibana
1. Open Kibana at http://localhost:5601
2. Go to Stack Management → Index Patterns
3. Create a new index pattern:
```
flask-logs*
```
4. Go to Discover to visualize the logs coming from your Flask app 🎉
---

## Stop & Cleanup

```bash
docker compose down -v
```

---
