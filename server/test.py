import json
from flask import Flask, jsonify, request, redirect

app = Flask(__name__)

@app.route('/',methods=['POST'])
def post():
        data = request.data
        json.dumps(data)
        return 'true'


app.run(host='0.0.0.0', port=8080)