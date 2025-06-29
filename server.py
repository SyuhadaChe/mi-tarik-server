from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

MENU_FILE = "menu.json"
ORDER_FILE = "website_orders.json"

@app.route("/menu", methods=["GET", "POST"])
def menu():
    if request.method == "GET":
        if os.path.exists(MENU_FILE):
            with open(MENU_FILE, "r") as f:
                return jsonify(json.load(f))
        else:
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
        return jsonify({"status": "added"})


@app.route("/order", methods=["POST"])
def order():
    data = request.get_json()
    if os.path.exists(ORDER_FILE):
        with open(ORDER_FILE, "r") as f:
            orders = json.load(f)
    else:
        orders = []

    orders.append(data)
    with open(ORDER_FILE, "w") as f:
        json.dump(orders, f, indent=2)

    return jsonify({"status": "received"})


@app.route("/orders", methods=["GET"])
def get_orders():
    if os.path.exists(ORDER_FILE):
        with open(ORDER_FILE, "r") as f:
            return jsonify(json.load(f))
    else:
        return jsonify([])

