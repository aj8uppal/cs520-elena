from flask import Flask, jsonify, request
import sys
sys.path.append('../model')

from model import EleNa

app = Flask(__name__)

@app.route('/compute_shortest_path', methods=['POST'])
def compute_shortest_path():
    body = request.json
    start = body["start"]
    end = body["end"]
    alg = body["alg"] if "alg" in body else "default"
    E = EleNa([start["latitude"], start["longitude"]], [end["latitude"], end["longitude"]], alg=alg)
    path = E.shortest_path_custom()
    return jsonify(path)
