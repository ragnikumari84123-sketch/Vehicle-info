from flask import Flask, request, jsonify
from vehicle_lookup import vehicle

app = Flask(__name__)

@app.route("/")
def home():
    return "API is running 🚀"

@app.route("/vehicle")
def vehicle_api():
    number = request.args.get("number")
    if not number:
        return jsonify({"error": "number missing"})

    data = vehicle(number)
    return jsonify(data)

