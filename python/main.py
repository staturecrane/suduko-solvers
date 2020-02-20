from flask import Flask, jsonify, request
from flask_cors import CORS

from solver import solver

app = Flask(__name__)


@app.route("/puzzle/solve", methods=["POST"])
def solve_puzzle():
    request_data = request.get_json()
    starting = request_data.get("starting", [])

    board_values = solver(starting)

    return jsonify({"board_values": board_values})
