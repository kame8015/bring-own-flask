from __future__ import print_function
import os
from PIL import Image, ImageOps
import io
import flask

# import boto3

# The flask app for serving predictions
app = flask.Flask(__name__)

# s3 = boto3.resource("s3")
# bucket = s3.Bucket("kame-sagemaker-test")

prefix = "/opt/ml/"
model_path = os.path.join(prefix, "model")

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENTIONS = set(["jpg", "jpeg"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


class ScoringService(object):
    model = None  # Where we keep the model when it's loaded

    @classmethod
    def get_model(cls):

        if cls.model == None:
            with open(os.path.join(model_path, "model.txt"), encoding="utf-8") as file:
                cls.model = file.read()
        return cls.model

    @classmethod
    def predict(cls, input):

        text = cls.get_model()
        text += input

        # ここで detectionCrackPy に画像パスを渡す
        return text


@app.route("/ping", methods=["GET"])
def ping():
    health = ScoringService.get_model() is not None

    status = 200 if health else 404
    return flask.Response(response="\n", status=status, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def transformation():
    # データの取り出し
    if flask.request.content_type == "application/x-image":
        print("reading input file...")
        img_binary = flask.request.data
        img = Image.open(io.BytesIO(img_binary)).convert("RGB")
        img_invert = ImageOps.invert(img)

        # 画像からバイナリに変換
        with io.BytesIO() as output:
            img_invert.save(output, format="JPEG")
            img_invert_binary = output.getvalue()

    response = flask.make_response(img_invert_binary)
    response.headers.set("Content-Type", "image/jpeg")

    print("Inverted!!!!!")

    return response
