from flask import Flask, jsonify, request, redirect

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def catch_all(path):
        print("Path: {}".format(path))
        print("Request Body: {}".format(request.body.raw))
        return 'true'


app.run(host='0.0.0.0', port=8080)