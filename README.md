# TODO APP API

## 概要

TODOアプリ用のAPIの実装例です。FastAPI + Uvicorn 構成で実装し、コンテナで動かします。  
現時点では、データストレージにAWS DynamoDBを想定した実装になっています。  
ローカルのDocker環境では、DynamoDB-Localを使用して動作確認できるようにしています。

## 構成

### アーキテクチャ

![アーキテクチャ](/images/Architecture.png)

### ディレクトリ構成

```
.
├── app ............................................. アプリケーションルートディレクトリ
│   ├── core ........................................ 共通機能
│   ├── crud ........................................ ストレージCRUD操作
│   ├── database .................................... ストレージ関連
│   ├── models ...................................... ストレージ用モデル
│   ├── routers ..................................... APIルーター
│   ├── schemas ..................................... APIルーターのスキーマ
│   ├── services .................................... ビジネスロジック
│   ├── dependencies.py ............................. APIルーターの依存関係定義
│   ├── config.py ................................... アプリケーション設定関連
│   └──  main.py .................................... エントリポイント
├── db .............................................. データベース関連
│   └── dynamodb .................................... DynamoDB関連（Seedデータ等） 
├── images .......................................... README用画像ディレクトリ
├── tests ........................................... PyTestコードルートディレクトリ
├── compose.yaml .................................... ローカル環境用構築用 Comose File
├── Dockerfile ...................................... AWS Lambda用 Dockerfile
├── Dockerfile.local ................................ ローカル環境用 Dockerfile
├── openapi.json .................................... OAS形式のAPIドキュメント
├── openapi.py ...................................... FastAPIからOAS形式のAPIドキュメント出力するスクリプト
├── poetry.lock ..................................... poetryのlockファイル
├── poetry.toml ..................................... poetryの設定ファイル
├── pyproject.toml .................................. poetryのプロジェクト定義ファイル（依存関係等）
├── README.md ....................................... README
└── ServerlessApp.yaml .............................. Cloudformationテンプレート
```

## 構築手順

### 前提条件

AWS CLIをセットアップ済みであること。

### Docker環境

[FastAPI](https://fastapi.tiangolo.com/ja/)アプリケーション、
[DynamoDB Local](https://hub.docker.com/r/amazon/dynamodb-local)、
[Dynamodb Admin](https://github.com/aaronshaf/dynamodb-admin)
を起動します。

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

Swagger UI (http://127.0.0.1:8080/docs) から動作確認ができます。  
本実装例では、疑似的な認証を実装しています。 アプリケーションは、Authorizationヘッダからユーザー名を取得して処理を行います。  
下記のようにAuthorizationヘッダを設定して実行してください。

[ヘッダ定義例]

```
"Authorization": "Bearer user001"
```

[Swagger UI]

![Swagger UIで設定する例](/images/SwaggerUI-Authorization.png)


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


#### API Gatewayのエンドポイントについて

リソースポリシーは設定していません。

#### Lambda関数URLについて

Lambdaの関数URLが作成されますが、リソースベースのポリシーは設定していません。  
そのままではAPIドキュメントにアクセスできません。アクセスする場合は、リソースベースのポリシーで許可設定を追加します。  
※ URLを知っている人なら誰でもアクセスできるようになる点に注意

[マネージメントコンソールからの手順]

1. 当該Lambda関数の画面を開く
2. 「設定」タブを選択
3. 左メニューの「アクセス権限」を選択
4. 「リソースベースのポリシーステートメント」セクションの「アクセス権限を追加」をクリック
5. 「関数URL」を選択、認証タイプに「None」を選択して、「保存」する


## APIドキュメント

上述した通り、APIドキュメントはFastAPIを起動することで確認可能です。  
OAS形式のファイルは `openapi.json` です。  
API仕様を更新した場合は、 `openapi.py` を実行することで `openapi.json` を更新できます。  
