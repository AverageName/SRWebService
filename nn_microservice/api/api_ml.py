import flask
from flask import request, jsonify
import base64
import io
import numpy as np
from ml import predict_sr
from PIL import Image
from io import BytesIO

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['POST'])
def predict():
    values = request.json
    image_b64 = values['img']
    id = values['id']
    stream = BytesIO(base64.b64decode(image_b64))
    image = Image.open(stream).convert("RGBA")
    stream.close()
    img = np.array(image)
    # img = base64.b64decode(img)
    # img = np.frombuffer(img, dtype=np.uint8)
    # img = np.reshape(img, shape)
    result = predict_sr(img)

    # result = np.ascontiguousarray(result)
    shape = list(result.shape)
    img = Image.fromarray(result)
    buff = BytesIO()
    img.save(buff, format="JPEG")
    result_b64 = base64.b64encode(buff.getvalue()).decode("utf-8")

    return jsonify({"response": 200,
            "id": id,
            "shape": shape,
            "img": result_b64})

app.run(host="0.0.0.0", port=5001, debug=True)