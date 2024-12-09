from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/price", methods=["GET"])
def get_price():
    # Example price feed
    price_in_usd = 0.10  # Price of 1 token in USD
    return jsonify({
        "symbol": "NXC",
        "price": price_in_usd
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
