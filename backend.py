import stripe
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["worlwishesdb"]
products_collection = db["products"]
orders_collection = db["orders"]

STRIPE_PUBLISHABLE_KEY = "pk_test_51NzOH5HkEYR9UeV6hiF7CVQcOi7vl2R4ghGFe6F0z1sewFWZqy0jYq5yeqUnlcIZLdUvFntmsVGHxsfLGV7X8pEQ00FixKoEMl"
STRIPE_SECRET_KEY = "sk_test_51NzOH5HkEYR9UeV60fvE0jFo9JofTo1ZQIwPBB3Qq8K9J7BOWsyHypj0mUcfpaKJ4vxW298xLkpEkb0LjceZo8IP00QQxur3MT"

stripe.api_key = STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://localhost:3000'


@app.route("/products", methods=["POST"])
def insert_product():
    data = request.json
    product_id = products_collection.insert_one(data).inserted_id
    return jsonify({"message": "product inserted", "product_id": str(product_id)}), 201


@app.route("/products", methods=["GET"])
def get_products():
    products = list(products_collection.find({}))
    for product in products:
        product["_id"] = str(product["_id"])
    return jsonify(products)


@app.route("/order", methods=["POST"])
def insert_order():
    data = request.json
    order_id = orders_collection.insert_one(data).inserted_id
    return jsonify({"message": "product inserted", "product_id": str(order_id)}), 201


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            ui_mode='embedded',
            billing_address_collection='required',
            line_items=[
                {
                    'price': 'price_1NzOc1HkEYR9UeV6I4BeUk1q',
                    'quantity': 1,
                },
            ],
            mode='payment',
            return_url=YOUR_DOMAIN + '/return?session_id={CHECKOUT_SESSION_ID}',
        )
    except Exception as e:
        print(str(e))
    return jsonify(clientSecret=session.client_secret)


@app.route('/get-session-status-given-id', methods=["POST"])
def get_session_status_given_id():
    data = request.json
    current_id = data["checkout_session_id"]

    try:
        checkout_session = stripe.checkout.Session.retrieve(current_id)
        payment_status = checkout_session['payment_status']
        return jsonify({"payment_status": payment_status}), 201
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
