import time

from boto3.session import Session


class SagemakerClient:
    def __init__(self):
        self.client = Session(profile_name="kameda").client(
            "sagemaker", region_name="ap-northeast-1"
        )
        sts = Session(profile_name="kameda").client("sts")
        self.account_id = sts.get_caller_identity()["Account"]

    def create_model(self, model_data_url):
        timestamp = time.strftime("%Y%m%d-%H%M%S")

        model_params = {
            "ExecutionRoleArn": f"arn:aws:iam::{self.account_id}:role/service-role/AmazonSageMaker-ExecutionRole-20210517T171336",  # noqa: errors
            "ModelName": f"flask-sample-{timestamp}",  # モデル名
            "PrimaryContainer": {
                "Image": f"{self.account_id}.dkr.ecr.ap-northeast-1.amazonaws.com/flask_test:latest",  # ECRにプッシュしたイメージURL # noqa: errors
                "ModelDataUrl": model_data_url,  # モデルデータが格納されているS3のパス
            },
        }

        self.client.create_model(**model_params)

        print("model created!")


if __name__ == "__main__":

    model_data_url = f"s3://kame-sagemaker-flask/model/model.tar.gz"
    SagemakerClient().create_model(model_data_url)
