from flask import Flask, jsonify
import json

app = Flask(__name__)


@app.route("/hello", methods=["GET"])
def hello_word():
    return "Hello World!"


@app.route("/view-data", methods=["GET"])
def viewData():
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com'})

@app.route("/sample", methods=["GET"])
def nextFunction():
    text = "Hello World and welcome to flask world!!"
    return jsonify(text)

app.run(debug=True)
a = 7+54

