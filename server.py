#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      hadac
#
# Created:     29/06/2025
# Copyright:   (c) hadac 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

ORDERS_FILE = "website_orders.json"

@app.route('/order', methods=['POST'])
def save_order():
    try:
        data = request.get_json()

        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, 'r') as f:
                orders = json.load(f)
        else:
            orders = []

        orders.append(data)

        with open(ORDERS_FILE, 'w') as f:
            json.dump(orders, f, indent=2)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Mi Tarik Server is running!"

if __name__ == '__main__':
    app.run()
