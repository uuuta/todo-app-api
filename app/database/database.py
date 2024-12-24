from typing import Annotated

from fastapi import Depends

from config import settings
from crud.task import TaskDBClient
from crud.task_dynamodb import DynamoDBTaskClient


def get_task_database() -> TaskDBClient:
    if settings.dynamodb_endpoint is not None:
        return DynamoDBTaskClient(settings.aws_region, settings.dynamodb_task_table_name,
                                  settings.dynamodb_endpoint)
    return DynamoDBTaskClient(settings.aws_region, settings.dynamodb_task_table_name)


TaskDatabaseDep = Annotated[TaskDBClient, Depends(get_task_database)]
