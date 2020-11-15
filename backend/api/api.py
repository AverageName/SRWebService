import flask
from flask import request, jsonify, make_response
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

app = flask.Flask(__name__)
app.config["DEBUG"] = True

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
        # print(request.files, file=sys.stderr)
        # print(request.data, file=sys.stderr)
        # print(request.json, file=sys.stderr)
        # print(request.form, file=sys.stderr)
        values = request.data
        # print(type(values), file=sys.stderr)
        # print(values, file=sys.stderr)
        # print(values['photo'], file=sys.stderr)
        #image_bytes = values.read()
        image_base64 = json.loads(values.decode('utf-8'))['photo']
        image_base64 = image_base64.replace('data:image/jpeg;base64,', '')
        print(type(image_base64), file=sys.stderr)
        # stream = BytesIO(image_bytes)
        # image = Image.open(stream).convert("RGBA")
        # stream.close()

        #print(type(image), file=sys.stderr)
        #width, height = im
        if image_base64 is not None:
            id = str(uuid.uuid4())
            response = jsonify({
                "response": 200,
                "id": id
            })
            db.add_image(id=id, image=image_base64)
        else:
            response = jsonify({
                "response": 401
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
        print("Hello world", file=sys.stderr)
        req = db.images.find_one({"id": img_id})
        print("Hello world", file=sys.stderr)

        ret = requests.post('http://172.17.0.1:5001/', json={
                                                            "id": img_id,
                                                            "img": req['image'],
                                                            })
        print("Hello world", file=sys.stderr)
        data = ret.json()
        print("Hello world", file=sys.stderr)

        response = jsonify({"response": 200,
                "img": data["img"],
                "new_shape": data["shape"]
                })

        response.headers.add("Access-Control-Allow-Origin", "*")

        return response


app.run(host="0.0.0.0", debug=True)
