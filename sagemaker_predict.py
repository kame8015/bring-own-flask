import time

from boto3.session import Session


class SagemakerClient:
    def __init__(self):
        self.client = Session(profile_name="kameda").client(
            "sagemaker", region_name="ap-northeast-1"
        )

    def submit_transform_job(self):

        model_name = self.client.list_models(
            NameContains="flask-sample",  # 各自デプロイしたモデル名に含まれている文字列
            SortOrder="Descending",
            SortBy="CreationTime",
        )["Models"][0]["ModelName"]

        timestamp = time.strftime("%Y%m%d-%H%M%S")

        transform_params = {
            "TransformJobName": "sample-" + timestamp,  # 　バッチ変換ジョブ名
            "ModelName": model_name,  # デプロイしたモデル名
            # "BatchStrategy": "MultiRecord",
            "MaxConcurrentTransforms": 1,
            "MaxPayloadInMB": 50,
            "TransformInput": {
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": "s3://kame-sagemaker-flask/predict/input/",  # 推論を行うインプットデータが格納されているS3パス  # noqa: errors
                    }
                },
                "ContentType": "application/x-image",
                # "SplitType": "Line",
            },
            "TransformOutput": {
                "S3OutputPath": "s3://kame-sagemaker-flask/predict/output/"  # 推論結果を格納するS3パス
            },
            "TransformResources": {"InstanceType": "ml.m4.xlarge", "InstanceCount": 1},
        }

        self.client.create_transform_job(**transform_params)

        print("start predict!")


if __name__ == "__main__":
    SagemakerClient().submit_transform_job()
