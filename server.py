
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory order list
orders = []

@app.route("/")
def home():
    return "✅ Mi Tarik Server is running."

@app.route("/order", methods=["POST"])
def receive_order():
    try:
        data = request.get_json()
        orders.append(data)
        return jsonify({"message": "Order received and stored."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
