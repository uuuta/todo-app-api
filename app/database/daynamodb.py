from abc import ABC, abstractmethod
import boto3


class DynamoDBResource:
    def __init__(self, table_name: str, region: str):
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.table = self.dynamodb.Table(table_name)
