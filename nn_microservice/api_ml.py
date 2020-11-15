import sys
sys.path.append('./DRLN/')
import flask
from flask import request, jsonify
import base64
import io
import numpy as np
from ESRGAN.ml import predict_sr as predict_sr_esrgan
from PIL import Image
from io import BytesIO
from DRLN.run_model import predict_sr as predict_sr_drln

sr_models = {"ESRGAN": predict_sr_esrgan,
             "DRLN": predict_sr_drln}


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['POST'])
def predict():
    values = request.json
    image_b64 = values['img']
    id = values['id']

    try:
        stream = BytesIO(base64.b64decode(image_b64))
        image = Image.open(stream).convert("RGBA")
        stream.close()
        img = np.array(image)
    except Exception as e:
        response = jsonify({
            "status": 401,
            "error": e
        })
        return response

    try:
        result = sr_models["DRLN"](img)
        #print(result, file=sys.stderr)
    except Exception as e:
        response = jsonify({
            "status": 401,
            "error": e
        })
        return response

    try:
        shape = list(result.shape)
        img = Image.fromarray(result)
        buff = BytesIO()
        img.save(buff, format="JPEG")
        result_b64 = base64.b64encode(buff.getvalue()).decode("utf-8")
        #print(result_b64, file=sys.stderr)
    except Exception as e:
        response = jsonify({
            "status": 401,
            "error": e
        })
        return response

    return jsonify({"status": 200,
            "id": id,
            "shape": shape,
            "img": result_b64})

app.run(host="0.0.0.0", port=5001, debug=True)