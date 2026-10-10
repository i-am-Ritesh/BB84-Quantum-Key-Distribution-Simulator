from flask import Flask, request, jsonify
from flask_cors import CORS
from bb84 import BB84Simulator
app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return jsonify({
        "application": "BB84 Quantum Key Distribution Simulator",
        "status": "Running"
    })
@app.route("/simulate", methods=["POST"])
def simulate():
    try:
        data = request.get_json(silent=True) or {}
        simulator = BB84Simulator(
            num_bits=int(data.get("num_bits", 32)),
            eve=bool(data.get("eve", False)),
            noise_probability=float(data.get("noise_probability", 0.0))
        )
        result = simulator.run()
        return jsonify({
            "success": True,
            "simulation": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )