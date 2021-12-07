from flask import Flask, jsonify, request, send_from_directory
import sys, os
sys.path.append('../model')

from model import EleNa

app = Flask(__name__, static_folder='build')

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

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
