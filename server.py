from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

ORDERS_FILE = "website_orders.json"
MENU_FILE = "menu.json"

# Ensure files exist if not present
def ensure_file_exists(path, default):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f)

ensure_file_exists(ORDERS_FILE, [])
ensure_file_exists(MENU_FILE, [])

@app.route("/order", methods=["POST"])
def submit_order():
    try:
        new_order = request.get_json()
        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)
        orders.append(new_order)
        with open(ORDERS_FILE, "w") as f:
            json.dump(orders, f, indent=2)
        return jsonify({"message": "Order received"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/orders", methods=["GET"])
def get_orders():
    try:
        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/menu", methods=["GET"])
def get_menu():
    try:
        with open(MENU_FILE, "r") as f:
            menu = json.load(f)
        return jsonify(menu)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/menu", methods=["POST"])
def add_menu_item():
    try:
        new_item = request.get_json()
        with open(MENU_FILE, "r") as f:
            menu = json.load(f)
        menu.append(new_item)
        with open(MENU_FILE, "w") as f:
            json.dump(menu, f, indent=2)
        return jsonify({"message": "Menu item added"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/menu/delete", methods=["POST"])
def delete_menu_item():
    try:
        data = request.get_json()
        item_id = data.get("id")
        with open(MENU_FILE, "r") as f:
            menu = json.load(f)
        updated_menu = [item for item in menu if item.get("id") != item_id]
        with open(MENU_FILE, "w") as f:
            json.dump(updated_menu, f, indent=2)
        return jsonify({"message": "Item deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Mi Tarik Server is running."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


       
