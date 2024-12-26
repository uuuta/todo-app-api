import json
import os

import boto3
import pytest
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# .envファイルの内容を読み込む
load_dotenv()

current_path = os.getcwd()
project_root = current_path[:current_path.find("tests")] if current_path.find("tests") > 0 else current_path


@pytest.fixture(scope="session")
def dynamodb_local():
    dynamodb = boto3.resource('dynamodb',
                              region_name="ap-northeast-1",
                              endpoint_url="http://127.0.0.1:8000")
    try:
        with open(os.path.join(project_root, 'db', 'dynamodb', 'task_table.json')) as f:
            table_schema = json.load(f)
            table = dynamodb.create_table(**table_schema)
            table.meta.client.get_waiter('table_exists').wait(TableName='Tasks')
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("Table already exists. Skipping creation.")
            table = dynamodb.Table('tasks')
        else:
            raise e

    yield table
