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
