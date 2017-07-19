from flask import Flask, jsonify, request, redirect

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all():
        print("Path: {}".format(path))
        print(jsonify(request.json))
        return 'true'


app.run(host='0.0.0.0', port=8080)