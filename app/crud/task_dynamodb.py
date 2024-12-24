from typing import List
from uuid import UUID

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from core.logging import get_logger
from crud.task import TaskDBClient
from models.task import Task

logger = get_logger()


class DynamoDBTaskClient(TaskDBClient):
    def __init__(self, region: str, table_name: str, endpoint_url=None):
        if endpoint_url:
            self.dynamodb = boto3.resource("dynamodb", region_name=region, endpoint_url=endpoint_url)
        else:
            self.dynamodb = boto3.resource("dynamodb", region_name=region)
        self.table = self.dynamodb.Table(table_name)

    def create_task(self, task: Task) -> Task:
        # OptionalなフィールドはNoneの可能性がある
        task_dict = {k: v for k, v in task.model_dump(by_alias=True).items() if v is not None}
        item = {"userId": task.user_id, "taskId": str(task.task_id), **task_dict}
        logger.debug(item)
        try:
            self.table.put_item(Item=item)
        except ClientError as error:
            logger.error(error)
            raise
        return self.get_task_by_id(task.user_id, task.task_id)

    def get_task_list(self, user_id: str) -> List[Task]:
        logger.debug(f"{user_id}")
        try:
            response = self.table.query(
                KeyConditionExpression=Key("userId").eq(user_id)
            )
            logger.debug(response)
        except ClientError as error:
            logger.error(error)
            raise
        task_list = [Task(**item) for item in response.get("Items", [])]
        logger.debug(task_list)
        return task_list

    def get_task_by_id(self, user_id: str, task_id: UUID) -> Task | None:
        logger.debug(f"{user_id}, {task_id}")
        try:
            response = self.table.get_item(Key={"userId": user_id, "taskId": str(task_id)})
            logger.debug(response)
        except ClientError as error:
            logger.error(error)
            raise
        item = response.get("Item")
        if item is None:
            return None
        return Task(**item)

    def update_task(self, task: Task) -> Task | None:
        # 完了フラグ(done)は除外
        task_dict = {k: v for k, v in task.model_dump(by_alias=True).items() if k != "done" and v is not None}
        update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in task_dict.keys())
        expression_values = {f":{k}": v for k, v in task_dict.items()}
        logger.debug(f"task_dict={task_dict}"
                     f"update_expression={update_expression}"
                     f"expression_values={expression_values}")
        logger.debug(update_expression)
        try:
            response = self.table.update_item(
                Key={"userId": task.user_id, "taskId": str(task.task_id)},
                UpdateExpression=update_expression,
                ConditionExpression="attribute_exists(userId) AND attribute_exists(taskId)",
                ExpressionAttributeValues=expression_values,
                ReturnValues="ALL_NEW"
            )
            logger.debug(response)
        except ClientError as error:
            if error.response['Error']['Code'] == "ConditionalCheckFailedException":
                return None
            logger.error(error)
            raise
        return Task(**response["Attributes"])

    def delete_task(self, user_id: str, task_id: UUID) -> None:
        logger.debug(f"{user_id}, {task_id}")
        try:
            self.table.delete_item(Key={"userId": user_id, "taskId": str(task_id)})
        except ClientError as error:
            logger.error(error)
            raise
        return

    def update_done_flg(self, user_id: str, task_id: UUID, flg: bool):
        logger.debug(f"{user_id}, {task_id}, {flg} ")
        try:
            response = self.table.update_item(
                Key={"userId": user_id, "taskId": str(task_id)},
                UpdateExpression="SET done = :val",
                ExpressionAttributeValues={":val": flg},
                ReturnValues="ALL_NEW"
            )
            logger.debug(response)
        except ClientError as error:
            logger.error(error)
            raise
        return Task(**response["Attributes"])
