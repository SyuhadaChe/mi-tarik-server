
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

ORDERS_FILE = "website_orders.json"

# Load existing orders if file exists
def load_orders():
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

# Save order to JSON file
def save_order(order):
    orders = load_orders()
    orders.append(order)
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=2)

# Route to handle order submission from website
@app.route('/order', methods=['POST'])
def receive_order():
    try:
        order = request.json
        save_order(order)
        return jsonify({"message": "Order received!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional: root route
@app.route('/')
def home():
    return "Mi Tarik Station Order Server is running."

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Required for Render
    app.run(host='0.0.0.0', port=port)
