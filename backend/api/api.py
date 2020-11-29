import flask
from flask import request, jsonify, make_response, send_from_directory
from db import DataBase
import base64
import json
import io
import numpy as np
from PIL import Image
import uuid
import requests
import sys
from io import BytesIO
import os


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

db = DataBase()

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


@app.route('/static/<path:path>/', methods=["OPTIONS", "GET"])
def send_static(path):
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    else:
        response = make_response(send_from_directory('/backend/api/static/', path))
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route('/', methods=['GET'])
def home_page():
    return '''<h1> Hello world </h1>'''

@app.route('/add', methods=['POST', "OPTIONS"])
def add_image():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    else:
        values = request.data
        image_base64 = json.loads(values.decode('utf-8'))['photo']
        image_base64 = image_base64.replace('data:image/png;base64,', '')
        print(type(image_base64), file=sys.stderr)

        if image_base64 is not None:
            id = str(uuid.uuid4())
            response = jsonify({
                "status": 200,
                "id": id
            })
            db.add_image(id=id, image=image_base64)
        else:
            response = jsonify({
                "status": 401,
                "error": "There is no image loaded"
                }
            )

        return response

@app.route('/use_nn', methods=['GET', 'OPTIONS'])
def predict():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    else:
        img_id = request.args.get("id")
        model_type = request.args.get("type")
        req = db.images.find_one({"id": img_id})

        if req is None:
            response = jsonify({
                "status": 401,
                "error": "There is no image with such id"
            })

            return response

        ret = requests.post('http://172.17.0.1:5001/', json={
                                                            "id": img_id,
                                                            "img": req['image'],
                                                            "model_type": model_type
                                                            })
        data = ret.json()
        if data['status'] != 200:
            response = jsonify({
                "status": 401,
                "error": data['error']
            })

            return response

        response = jsonify({"status": 200,
                "img": data["img"],
                "new_shape": data["shape"]
                })

        print(response, file=sys.stderr)
        print(response.headers, file=sys.stderr)

        return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
