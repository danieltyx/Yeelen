from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/data', methods=["POST"])
def add_guide():
    print(request.json)

    return ""