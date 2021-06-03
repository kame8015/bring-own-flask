# SageMaker での挙動確認

S3 の`kame-sagemaker-flask`バケットの
`/model/model.tar.gz`を読み込み、
`/predict/input/`配下にあるファイルを使って、
色反転した画像を`/predict/output/`に書き出す。

1. `~/.aws/credentials`に アクセスキー ID と シークレット を書いておく
   ```
   $ aws configure --profile {profile_name}
   AWS Access Key ID: ********************
   AWS Secret Access Key: ********************
   Default region name [None]: ap-northeast-1
   Default output format [None]: json
   ```
1. `flask_test` という Docker イメージを作成して ECR にプッシュする
   ```
   $ cd container
   $ ./build_and_push.sh flask_test {profile_name}
   $ cd ../
   ```
1. ECR の画面でイメージが登録されていることを確認する
1. S3 に bucket とフォルダを作成する
   - 親となる bucket: kame-sagemaker-flask(以後はこの下に作成)
   - モデルを格納しておくフォルダ: `/model`
   - 推論処理に使用されるインプットフォルダ: `/predict/input`
   - 推論後のアウトプットフォルダ: `/predict/output`
1. S3 にモデル、インプットファイルをアップロードする
   - モデル: `/model/model.tar.gz` (中身は`model.txt`)
   - インプットファイル:
     - `/predict/input/cat.jpg`
     - `/predict/input/dog.jpg`
1. 仮想環境を作って `requirements.txt` を pip install する
   ```
   $ python -m venv .venv
   $ source .venv/bin/activate
   $ pip install -r requirements.txt
   ```
1. ECR に登録されたイメージと S3 にアップロードされたモデルファイルを使用して、SageMaker のモデルをデプロイする
   ```
   $ python sagemaker_deploy.py
   ```
1. SageMaker の「モデル」に新しく作成されているのを確認する
1. SageMaker にデプロイされたモデルを使用して、バッチ推論ジョブを起動する
   ```
   $ python sagemaker_predict.py
   ```
1. SageMaker の「バッチ変換ジョブ」に新しいジョブが作成されていることを確認する
1. 終わったら、S3 の`kame-sagemaker-flask/predict/output/`に`cat.jpg.out`と`dog.jpg.out`が出力されていることを確認する
1. それぞれの`.out`を削除して、きちんと画像が色反転されていることを確認する
