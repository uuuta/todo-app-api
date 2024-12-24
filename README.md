# TODOアプリ（API） on AWS

## 概要

モノレポやめる

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
をDockerコンテナで起動してます。

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


### AWS環境
