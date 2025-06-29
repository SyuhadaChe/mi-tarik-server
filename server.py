from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import qrcode
from tkinter import messagebox, Tk, simpledialog
import requests

app = Flask(__name__)
CORS(app)

ORDERS_FILE = "website_orders.json"
MENU_FILE = "menu.json"

# Ensure data files exist
if not os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(MENU_FILE):
    with open(MENU_FILE, "w") as f:
        json.dump([], f)

@app.route("/order", methods=["POST"])
def receive_order():
    try:
        data = request.json
        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)
        orders.append(data)
        with open(ORDERS_FILE, "w") as f:
            json.dump(orders, f, indent=2)
        return jsonify({"message": "Order received"})
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
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/menu", methods=["POST"])
def add_menu_item():
    try:
        new_item = request.json
        if not all(key in new_item for key in ["id", "name", "price", "image_url"]):
            return jsonify({"error": "Missing one or more required fields."}), 400
        with open(MENU_FILE, "r") as f:
            current_menu = json.load(f)
        current_menu.append(new_item)
        with open(MENU_FILE, "w") as f:
            json.dump(current_menu, f, indent=2)
        return jsonify({"message": "Menu item added"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def show_gui_popup():
    try:
        url = "https://syuhadache.github.io/Mi-Tarik-Menu"
        qr = qrcode.make(url)
        qr.save("qr_temp.png")

        root = Tk()
        root.withdraw()  # Hide main window
        messagebox.showinfo("Scan QR", f"Scan the QR code to view menu:\n{url}")
        os.system("start qr_temp.png")

        admin_pw = simpledialog.askstring("Admin", "Enter admin password:", show='*')
        if admin_pw == "admin123":
            try:
                response = requests.get("https://mi-tarik-server.onrender.com/orders")
                if response.status_code == 200:
                    orders = response.json()
                    order_text = "\n\n".join([
                        f"Order by {o['name']} ({o['type']}):\n" +
                        "\n".join(f"- {item['name']} - RM{item['price']:.2f}" for item in o['items']) +
                        f"\nTotal: RM{o['total']:.2f}"
                        for o in orders
                    ])
                    messagebox.showinfo("Website Orders", order_text or "No orders found.")
                else:
                    messagebox.showerror("Error", f"Failed to fetch orders. Status: {response.status_code}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch orders.\n{e}")
        root.destroy()
    except Exception as e:
        print(f"⚠️ QR popup failed: {e}")

if __name__ == "__main__":
    print("\n🔗 Server running at: http://127.0.0.1:5000")
    show_gui_popup()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
