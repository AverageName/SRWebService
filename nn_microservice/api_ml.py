import sys
sys.path.append('./DRLN/')
sys.path.append('./CSNLN/')
sys.path.append('./CSNLN/model/')
import flask
from flask import request, jsonify
import base64
import io
import numpy as np
from PIL import Image
from io import BytesIO
from ESRGAN.ml import predict_sr as predict_sr_esrgan
from DRLN.run_model import predict_sr as predict_sr_drln
from CSNLN.run_model import predict_sr as predict_sr_csnln

sr_models = {"ESRGAN": predict_sr_esrgan,
             "DRLN": predict_sr_drln,
             "CSNLN": predict_sr_csnln}


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['POST'])
def predict():
    values = request.json
    image_b64 = values['img']
    id = values['id']
    model_type = values['model_type']

    try:
        stream = BytesIO(base64.b64decode(image_b64))
        image = Image.open(stream).convert("RGBA")
        stream.close()
        img = np.array(image)
    except Exception as e:
        response = jsonify({
            "status": 401,
            "error": str(e)
        })
        return response

    try:
        result = sr_models[model_type](img)
        #print(result, file=sys.stderr)
    except Exception as e:
        response = jsonify({
            "status": 401,
            "error": str(e)
        })
        return response

    try:
        shape = list(result.shape)
        img = Image.fromarray(result)
        buff = BytesIO()
        img.save(buff, format="PNG")
        result_b64 = base64.b64encode(buff.getvalue()).decode("utf-8")
        #print(result_b64, file=sys.stderr)
    except Exception as e:
        response = jsonify({
            "status": 401,
            "error": str(e)
        })
        return response

    return jsonify({"status": 200,
            "id": id,
            "shape": shape,
            "img": result_b64})

app.run(host="0.0.0.0", port=5001, debug=True)