from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

MENU_FILE = "menu.json"
ORDERS_FILE = "website_order.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return []

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    return "Mi Tarik Server is running"

@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(load_data(MENU_FILE))

@app.route('/menu', methods=['POST'])
def add_menu():
    menu = load_data(MENU_FILE)
    item = request.json
    menu.append(item)
    save_data(MENU_FILE, menu)
    return jsonify({"status": "success"})

@app.route('/menu/delete', methods=['POST'])
def delete_menu():
    menu = load_data(MENU_FILE)
    data = request.json
    item_id = data.get("id")
    updated_menu = [item for item in menu if item.get("id") != item_id]
    save_data(MENU_FILE, updated_menu)
    return jsonify({"status": "deleted"})

@app.route('/order', methods=['POST'])
def place_order():
    orders = load_data(ORDERS_FILE)
    order = request.json

    # Ensure payment info is structured correctly
    if 'payment' not in order:
        order['payment'] = {"method": "unknown"}
    else:
        payment = order['payment']
        payment.setdefault("method", "unknown")
        if payment['method'].lower() == "fpx":
            payment.setdefault("bank", "")
            payment.setdefault("username", "")
            payment.setdefault("password", "")

    orders.append(order)
    save_data(ORDERS_FILE, orders)
    return jsonify({"status": "received"})

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(load_data(ORDERS_FILE))

if __name__ == '__main__':
    app.run(debug=True)
