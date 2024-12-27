# TODO APP API

## 概要

TODOアプリ用のAPIです。
FastAPI + Uvicorn 構成をDockerコンテナ化しています。
現時点では、データストレージにAWS DynamoDBを想定した実装になっています。
ローカルのDocker環境では、DynamoDB-Localを使用して動作確認できるようにしています。

## 構成

### アーキテクチャ

### ディレクトリ構成

## 構築手順

### 前提条件

AWS CLIをセットアップ済みであること。

### Docker環境

[FastAPI](https://fastapi.tiangolo.com/ja/)アプリケーション、
[DynamoDB Local](https://hub.docker.com/r/amazon/dynamodb-local)、
[Dynamodb Admin](https://github.com/aaronshaf/dynamodb-admin)
をDockerコンテナで起動します。

#### コンテナ起動

Dockerコンテナのビルド

```commandline
$ docker compose build
```

Dockerコンテナの起動

```commandline
$ docker compose up
```

#### エンドポイント

| APIルート         | URL                                                      |
|----------------|----------------------------------------------------------|
| APIルート         | [http://127.0.0.1:8080](http://127.0.0.1:8080)           |
| APIドキュメント      | [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs) |
| DynamoDB Local | [http://127.0.0.1:8000](http://127.0.0.1:8000)           |
| DynamoDB Admin | [http://127.0.0.1:8001](http://127.0.0.1:8001)           |


#### テーブル作成

```commandline
$ aws dynamodb create-table --cli-input-json file://db/dynamodb/task_table.json --endpoint-url http://127.0.0.1:8000
```

#### テストデータ投入

```commandline
$ aws dynamodb batch-write-item --request-items file://db/dynamodb/task_seed.json --endpoint-url http://127.0.0.1:8000
```

#### 動作確認

Swagger UI(http://127.0.0.1:8080/docs)から動作確認ができます。


#### 開発環境作成

1. 仮想環境作成およびライブラリインストール
   ```commandline
   # プロジェクトルートで実行
   $ poetry install
   ```
2. 環境変数ファイルの準備
   ```commandline
   $ cp .env.example .env
   ```

#### テスト実行

事前にDynamoDB Localコンテナを起動してpytestを実行します。

```
$ pytest -s -x
```

### AWS環境

aws cliで構築する手順です。

[事前準備]
* CloudFormation向けのサービスアカウントロールを作成
* ECRにリポジトリを作成してイメージをPushしておく

```commandline
aws cloudformation create-stack \
    --stack-name todo-api-stack \
    --template-body file://ServerlessApp.yaml \
    --parameters ParameterKey=ECRImageUri,ParameterValue=123456789012.dkr.ecr.ap-northeast-1.amazonaws.com/your-repository:latest \
    --capabilities CAPABILITY_IAM \
    --role-arn arn:aws:iam::123456789012:role/YoureServiceRole
```

#### エンドポイント

| APIルート         | URL                                                      |
|----------------|----------------------------------------------------------|
| APIルート         | {API Gatewayのエンドポイント}           |
| APIドキュメント      | {Lambdaの関数URL}/docs |

Lambdaの関数URLが作成されますが、リソースベースのポリシーは設定していません（コメントアウト）ので、そのままではAPIドキュメントにアクセスできません。
アクセスする場合は、リソースベースのポリシーで許可設定を追加します。
※ URLを知っている人なら誰でもアクセスできるようになる点に注意

```json
    {
      "Sid": "FunctionURLAllowPublicAccess",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "lambda:InvokeFunctionUrl",
      "Resource": "arn:aws:lambda:ap-northeast-1:6123456789012:function:FunctionName",
      "Condition": {
        "StringEquals": {
          "lambda:FunctionUrlAuthType": "NONE"
        }
      }
    }
```

## APIドキュメント

APIドキュメントはFastAPIを起動することで確認可能です。  
OAS形式のファイルは `openapi.json` です。  
API仕様を更新した場合は、 `openapi.py` を実行することで `openapi.json` を更新できます。  
