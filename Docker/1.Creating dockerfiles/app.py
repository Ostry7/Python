from flask import Flask, jsonify, request

app = Flask(__name__)

# przykładowe dane
items = [
    {"id": 1, "name": "Docker"},
    {"id": 2, "name": "DevOps"},
]

@app.route("/")
def home():
    return "Hello from Flask in Docker!"

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items)

@app.route("/items", methods=["POST"])
def add_item():
    data = request.json
    new_item = {"id": len(items) + 1, "name": data.get("name")}
    items.append(new_item)
    return jsonify(new_item), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
