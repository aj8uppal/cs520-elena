from flask import Flask, jsonify, request
import sys
sys.path.append('../model')

from controller import foo

app = Flask(__name__)

@app.route('/compute_shortest_path', methods=['POST'])
def compute_shortest_path():
    body = request.json
    start = body["start"]
    end = body["end"]
    return jsonify(foo(start, end))
