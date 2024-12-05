from flask import request, jsonify, send_file
from application import app


@app.route('/ping', methods=['GET'])
def response_ping():
    return jsonify({"status": "ok"}), 200


@app.route('/apply', methods=['POST'])
def parse():
    pass