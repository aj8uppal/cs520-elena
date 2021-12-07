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
    algs = ["max_elev", "min_elev", "max_elev_dist"] if alg == "default" else [alg]
    Es = [EleNa([start["latitude"], start["longitude"]], [end["latitude"], end["longitude"]], alg=alg) for alg in algs]
    paths = [E.shortest_path_custom() for E in Es]
    return jsonify(paths)
