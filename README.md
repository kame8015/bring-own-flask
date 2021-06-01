# Container 挙動確認

`this is model!!`と書かれた
`/opt/ml/model/sample.txt`  
の末尾に、`this is input!!`と書かれた
`/opt/ml/input/input.txt`の文字列を追記して、
`/opt/ml/output/predicted.txt`  
としてインメモリに保存する。

1. `predictor.py`の`predict`メソッドで読み込んでいるインプットファイルの名前を`input.txt`に修正する
1. Docker イメージを作成する
   ```
   $ cd container
   $ docker build -t image_test .
   ```
1. Docker コンテナを立ち上げて bash に入る(使用したコンテナは終了時に自動削除)
   ```
   $ docker run -it --rm image_test /bin/bash
   ```
1. コンテナ内ボリュームの`/opt/ml/model`に`sample.txt`がいることを確認する
   ```
   root@dda9409b7c43:/opt/program# cat ../ml/model/sample.txt
   this is model!!
   ```
1. コンテナ内ボリュームの`/opt/ml/input`に`input.txt`がいることを確認する
   ```
   root@dda9409b7c43:/opt/program# cat ../ml/input/input.txt
   this is input!!
   ```
1. ローカルでコンテナを起動して nginx サーバを立ち上げる
   ```
   $ docker run --name container_test -p 8080:8080 image_test serve
   ```
1. nginx サーバに ping を送り死活管理を行う
   ```
   $ curl http://localhost:8080/ping
   ```
1. nginx サーバに実行をリクエストする
   ```
   $ curl -X POST http://localhost:8080/invocations
   this is model!!this is input!!
   ```
1. nginx サーバを Cmd+C で終了する
1. ローカルでコンテナを起動して bash に入り、`opt/ml/output/predicted.txt`があることを確認する
   ```
   $ docker start container_test
   $ docker exec -it container_test /bin/bash
   root@defa1a5a3d0d:/opt/program# cat ../ml/output/predicted.txt
   this is model!!this is input!!
   ```

# SageMaker での挙動確認

S3 の`kame-sagemaker-txt`バケットの
`/model/model.tar.gz`を読み込み、
`/predict/input/input.txt`を使って、
`/predict/output/input.txt.out`を作り出す

1. `~/.aws/credentials`に アクセスキー ID と シークレット を書いておく
   ```
   $ aws configure --profile {profile_name}
   AWS Access Key ID: ********************
   AWS Secret Access Key: ********************
   Default region name [None]: ap-northeast-1
   Default output format [None]: json
   ```
1. `txt_test` という Docker イメージを作成して ECR にプッシュする
   ```
   $ cd container
   $ ./build_and_push.sh txt_test {profile_name}
   $ cd ../
   ```
1. ECR の画面でイメージが登録されていることを確認する
1. S3 に bucket とフォルダを作成する
   - 親となる bucket: kame-sagemaker-txt(以後はこの下に作成)
   - モデルを格納しておくフォルダ: `/model`
   - 推論処理に使用されるインプットフォルダ: `/predict/input`
   - 推論後のアウトプットフォルダ: `/predict/output`
1. S3 にモデル、インプットファイルをアップロードする
   - モデル: `/model/model.tar.gz` (中身は`sample.txt`)
   - インプットファイル: `/predict/input/sagemaker_input.txt`
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
1. 終わったら、S3 の`kame-sagemaker-txt`バケットに`/predict/output/sagemaker_input.txt.out`が出力されていることを確認する
   ```
   this is model!!SageMaker input File!!
   ```
