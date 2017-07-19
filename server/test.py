from flask import Flask, jsonify, request, redirect

app = Flask(__name__)

@app.route('/direct_messages/new',methods=['POST'])
def post():
        print(jsonify(request.json))
        return 'true'


app.run(host='0.0.0.0', port=8080)