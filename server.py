from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

MENU_FILE = "menu.json"
ORDERS_FILE = "website_orders.json"

# ---------- Load Menu ----------
@app.route("/menu", methods=["GET", "POST"])
def menu():
    if request.method == "GET":
        if os.path.exists(MENU_FILE):
            with open(MENU_FILE, "r") as f:
                return jsonify(json.load(f))
        return jsonify([])
    
    if request.method == "POST":
        data = request.get_json()
        if os.path.exists(MENU_FILE):
            with open(MENU_FILE, "r") as f:
                menu = json.load(f)
        else:
            menu = []
        menu.append(data)
        with open(MENU_FILE, "w") as f:
            json.dump(menu, f, indent=2)
        return jsonify({"status": "added", "item": data})


# ---------- Submit Order ----------
@app.route("/order", methods=["POST"])
def submit_order():
    try:
        data = request.get_json()
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, "r") as f:
                orders = json.load(f)
        else:
            orders = []
        orders.append(data)
        with open(ORDERS_FILE, "w") as f:
            json.dump(orders, f, indent=2)
        return jsonify({"status": "received", "order": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- View Orders ----------
@app.route("/orders", methods=["GET"])
def get_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as f:
            return jsonify(json.load(f))
    return jsonify([])

# ---------- Run Server ----------
if __name__ == "__main__":
    app.run(debug=False, port=5000)
