from boto3.session import Session


class S3Handler:
    def __init__(self):
        s3 = Session(profile_name="kameda").resource("s3")
        self.bucket = s3.Bucket("kame-sagemaker-test")

    def put(self, file_name, data):
        self.bucket.put_object(Key=file_name, Body=data)


if __name__ == "__main__":
    # bucket_obj = S3Handler().bucket

    data = open("./container/test_dir/predict/images/cat.jpg", "rb")
    S3Handler().put("cat.jpg", data)

    print("Put Succeeded!")