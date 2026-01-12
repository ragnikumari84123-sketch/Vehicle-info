from flask import Flask, request, jsonify
from vehicle_lookup import vehicle

app = Flask(__name__)

@app.route("/api/vehicle")
def get_vehicle():
    number = request.args.get("number")
    if not number:
        return jsonify({"error": "Vehicle number required"}), 400

    result = vehicle(number.upper())
    return jsonify({"data": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
