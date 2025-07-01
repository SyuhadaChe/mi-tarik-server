from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

MENU_FILE = "menu.json"
ORDERS_FILE = "orders.json"

def read_json(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)
    with open(file, 'r') as f:
        return json.load(f)

def write_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return "Mi Tarik Server is running!"

@app.route("/menu", methods=["GET", "POST"])
def menu():
    if request.method == "GET":
        return jsonify(read_json(MENU_FILE))
    elif request.method == "POST":
        new_item = request.json
        menu = read_json(MENU_FILE)
        menu.append(new_item)
        write_json(MENU_FILE, menu)
        return jsonify({"message": "Item added"}), 200

@app.route("/menu/delete", methods=["POST"])
def delete_menu():
    item_id = request.json.get("id")
    menu = read_json(MENU_FILE)
    new_menu = [item for item in menu if item["id"] != item_id]
    write_json(MENU_FILE, new_menu)
    return jsonify({"message": "Item deleted"}), 200

@app.route("/order", methods=["POST"])
def place_order():
    new_order = request.json
    orders = read_json(ORDERS_FILE)
    orders.append(new_order)
    write_json(ORDERS_FILE, orders)
    return jsonify({"message": "Order received"}), 200

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(read_json(ORDERS_FILE))

if __name__ == "__main__":
    app.run(debug=True)
