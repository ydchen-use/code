import time
import json

from flask import Flask, jsonify, request, abort

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/add_post", methods=["POST"])
def add_post():
    print(request.headers)
    print(type(request.json))
    print(request.json)
    result = request.json
    return str(result)


# @app.route("/post/<int:post_id>")
# def hello_world(post_id):
#     return "Post %d!" % post_id


if __name__ == "__main__":
    app.run(debug=True)
