from __future__ import print_function
import os
from PIL import Image, ImageOps
import io
import flask
import base64

# The flask app for serving predictions
app = flask.Flask(__name__)

prefix = "/opt/ml/"
model_path = os.path.join(prefix, "model")
input_path = os.path.join(prefix, "input")
output_path = os.path.join(prefix, "output")

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENTIONS = set(["jpg", "jpeg"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


class ScoringService(object):
    model = None  # Where we keep the model when it's loaded

    @classmethod
    def allowed_file(cls, filename):
        # 許可された拡張子だと1、でなければ0を返す
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENTIONS
        )

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        # if cls.model == None:
        #     with open(os.path.join(model_path, "decision-tree-model.pkl"), "rb") as inp:
        #         cls.model = pickle.load(inp)
        # return cls.model

        if cls.model == None:
            with open(os.path.join(model_path, "model.txt"), encoding="utf-8") as file:
                cls.model = file.read()
        return cls.model

    @classmethod
    def predict(cls, input):
        """For the input, do the predictions and return them.

        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        text = cls.get_model()
        text += input

        # ここで detectionCrackPy に画像パスを渡す
        return text


@app.route("/ping", methods=["GET"])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = ScoringService.get_model() is not None

    status = 200 if health else 404
    return flask.Response(response="\n", status=status, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None

    # txt/plain ファイルを読み込み．バイナリから文字列に変換
    # data = flask.request.get_data().decode("utf-8")

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

        # img_invert.save(os.path.join(output_path, "output.jpg"), format="jpeg")

    # Do the prediction
    # predictions = ScoringService.predict(data)

    # /opt/ml/output に書き出し
    # with open(os.path.join(output_path, "predicted.txt"), mode="w") as f:
    #     print("writing...")
    #     f.write(predictions)

    # result = open(os.path.join(output_path, "predicted.txt"))

    # response = flask.make_response(img_binary)
    response = flask.make_response(img_invert_binary)
    response.headers.set("Content-Type", "image/jpeg")

    print("Inverted!!!!!")

    # return flask.Response(response=response, status=200)
    return response
