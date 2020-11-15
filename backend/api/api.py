import flask
from flask import request, jsonify, make_response, send_from_directory
from db import DataBase
import base64
import json
import io
import numpy as np
# from ml import predict_sr
from PIL import Image
import uuid
import requests
import sys
from io import BytesIO
from flask_swagger_ui import get_swaggerui_blueprint
import os


app = flask.Flask(__name__)
# app._static_folder = "/backend/api/static/"
app.config["DEBUG"] = True

#Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route('/static/<path:path>', methods=["GET"])
def send_static(path):
    return send_from_directory('/backend/api/static', path)
## Swagger

db = DataBase()

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


@app.route('/', methods=['GET'])
def home_page():
    return '''<h1> Hello world </h1>'''

#Add convertion to base64 when adding new image
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

        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route('/use_nn', methods=['GET', 'OPTIONS'])
def predict():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    else:
        img_id = request.args.get("id")
        req = db.images.find_one({"id": img_id})

        if req is None:
            response = jsonify({
                "status": 401,
                "error": "There is no image with such id"
            })
            response.headers.add("Access-Control-Allow-Origin", "*")

            return response

        ret = requests.post('http://172.17.0.1:5001/', json={
                                                            "id": img_id,
                                                            "img": req['image'],
                                                            })
        # print(ret.data, file=sys.stderr)
        data = ret.json()
        if data['status'] != 200:
            response = jsonify({
                "status": 401,
                "error": data['error']
            })
            response.headers.add("Access-Control-Allow-Origin", "*")

            return response

        response = jsonify({"status": 200,
                "img": data["img"],
                "new_shape": data["shape"]
                })

        response.headers.add("Access-Control-Allow-Origin", "*")
        print(response, file=sys.stderr)
        print(response.headers, file=sys.stderr)

        return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
