from flask import Flask, jsonify, request, redirect
import json

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def catch_all(path):
        print("Path: {}".format(path))
        print("Request Body: {}".format(json.dumps(request.get_json())))
        return 'true'


app.run(host='0.0.0.0', port=8080)