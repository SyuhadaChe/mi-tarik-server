from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

menu = [
    {"id": 1, "name": "Beef Ramen", "price": 16.00, "image_url": "https://via.placeholder.com/150?text=Beef+Ramen"},
    {"id": 2, "name": "Fried Dumpling", "price": 12.00, "image_url": "https://via.placeholder.com/150?text=Fried+Dumpling"}
]

orders = []

@app.route("/")
def home():
    return "Welcome to Mi Tarik Server!"

@app.route("/menu", methods=["GET", "POST"])
def handle_menu():
    if request.method == "GET":
        return jsonify(menu)
    elif request.method == "POST":
        new_item = request.get_json()
        menu.append(new_item)
        return jsonify({"message": "Item added"}), 201

@app.route("/menu/delete", methods=["POST"])
def delete_menu_item():
    data = request.get_json()
    item_id = data.get("id")
    global menu
    menu = [item for item in menu if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

@app.route("/order", methods=["POST"])
def place_order():
    order = request.get_json()
    orders.append(order)
    return jsonify({"message": "Order received"}), 201

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)

if __name__ == "__main__":
    app.run(debug=True)
