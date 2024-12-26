import json
import os

import pytest
from botocore.exceptions import ClientError
from fastapi.testclient import TestClient

from app.main import app
from tests.conftest import project_root

client = TestClient(app)

USER001_SEED_DATA_SIZE = 2


@pytest.fixture
def user1_header():
    return {"Authorization": "Bearer user001"}


@pytest.fixture
def user2_header():
    return {"Authorization": "Bearer user002"}


@pytest.fixture
def task(dynamodb_local):
    def clear_all_items(table):
        response = dynamodb_local.scan()
        items = response.get('Items', [])
        with dynamodb_local.batch_writer() as batch:
            for item in items:
                batch.delete_item(
                    Key={
                        'userId': item['userId'],
                        'taskId': item['taskId']
                    }
                )

    clear_all_items(dynamodb_local)
    with open(os.path.join(project_root, 'db', 'dynamodb', 'task_seed.json')) as f:
        task_seed = json.load(f)["tasks"]
        tasks = []
        try:
            for data in task_seed:
                _item = data['PutRequest']['Item']
                task = {
                    "userId": _item["userId"]["S"],
                    "taskId": _item["taskId"]["S"],
                    "title": _item["title"]["S"],
                    "content": _item["content"]["S"],
                    "registrationDatetime": _item["registrationDatetime"]["S"],
                    "startDatetime": _item["startDatetime"]["S"],
                    "endDatetime": _item["endDatetime"]["S"],
                    "done": _item["done"]["BOOL"]
                }
                tasks.append(task)
                dynamodb_local.put_item(Item=task)
        except ClientError as e:
            print(e)
    yield tasks
    clear_all_items(dynamodb_local)


def test_list_tasks(user1_header, task):
    response = client.get("/tasks", headers=user1_header)
    assert response.status_code == 200

    resp = response.json()
    assert isinstance(resp, list)
    assert len(resp) == USER001_SEED_DATA_SIZE
    assert resp[0]["registrationDatetime"] > resp[1]["registrationDatetime"]


def test_list_tasks_sorted(user1_header, task):
    # desc
    response = client.get("/tasks?sort=desc", headers=user1_header)
    assert response.status_code == 200
    resp = response.json()
    assert resp[0]["registrationDatetime"] > resp[1]["registrationDatetime"]
    # asc
    response = client.get("/tasks?sort=asc", headers=user1_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    resp = response.json()
    assert resp[0]["registrationDatetime"] < resp[1]["registrationDatetime"]


def test_create_task(user1_header):
    new_task = {
        "title": "PyTest Task"
    }
    response = client.post("/tasks", json=new_task, headers=user1_header)
    assert response.status_code == 201
    resp = response.json()
    assert resp["title"] == new_task["title"]
    assert resp["content"] is None
    assert resp["registrationDatetime"] is not None
    assert resp["startDatetime"] is None
    assert resp["endDatetime"] is None
    assert resp["done"] is False

    new_task = {
        "title": "PyTest Task",
        "content": "PyTest content"
    }
    response = client.post("/tasks", json=new_task, headers=user1_header)
    assert response.status_code == 201
    resp = response.json()
    assert resp["title"] == new_task["title"]
    assert resp["content"] == new_task["content"]
    assert resp["registrationDatetime"] is not None
    assert resp["startDatetime"] is None
    assert resp["endDatetime"] is None
    assert resp["done"] is False

    new_task = {
        "title": "PyTest Task",
        "content": "PyTest content",
        "startDatetime": "2024-12-26 20:07:07"
    }
    response = client.post("/tasks", json=new_task, headers=user1_header)
    assert response.status_code == 201
    resp = response.json()
    assert resp["title"] == new_task["title"]
    assert resp["content"] == new_task["content"]
    assert resp["registrationDatetime"] is not None
    assert resp["startDatetime"] == new_task["startDatetime"]
    assert resp["endDatetime"] is None
    assert resp["done"] is False

    new_task = {
        "title": "PyTest Task",
        "content": "PyTest content",
        "startDatetime": "2024-12-26 20:07:07",
        "endDatetime": "2024-12-26 20:08:07"
    }
    response = client.post("/tasks", json=new_task, headers=user1_header)
    assert response.status_code == 201
    resp = response.json()
    assert resp["title"] == new_task["title"]
    assert resp["content"] == new_task["content"]
    assert resp["registrationDatetime"] is not None
    assert resp["startDatetime"] == new_task["startDatetime"]
    assert resp["endDatetime"] == new_task["endDatetime"]
    assert resp["done"] is False


def test_get_task(user2_header, task):
    task_id = "123e4567-e89b-12d3-a456-426614174002"
    response = client.get(f"/tasks/{task_id}", headers=user2_header)
    assert response.status_code == 200


def test_update_task(user2_header, task):
    task_id = "123e4567-e89b-12d3-a456-426614174002"
    response = client.get(f"/tasks/{task_id}", headers=user2_header)

    updated_task = response.json()
    updated_task["title"] = "Updated Task1"
    response = client.put(f"/tasks/{task_id}", json=updated_task, headers=user2_header)
    resp = response.json()
    assert resp["title"] == updated_task["title"]

    updated_task = response.json()
    updated_task["title"] = "Updated Task2"
    updated_task["content"] = "Updated content2"
    response = client.put(f"/tasks/{task_id}", json=updated_task, headers=user2_header)
    resp = response.json()
    assert resp["title"] == updated_task["title"]
    assert resp["content"] == updated_task["content"]

    updated_task = response.json()
    updated_task["title"] = "Updated Task3"
    updated_task["content"] = "Updated content3"
    updated_task["startDatetime"] = "2024-12-26 20:26:57"
    response = client.put(f"/tasks/{task_id}", json=updated_task, headers=user2_header)
    resp = response.json()
    assert resp["title"] == updated_task["title"]
    assert resp["content"] == updated_task["content"]
    assert resp["startDatetime"] == updated_task["startDatetime"]

    updated_task = response.json()
    updated_task["title"] = "Updated Task4"
    updated_task["content"] = "Updated content4"
    updated_task["startDatetime"] = "2024-12-26 21:26:57"
    updated_task["endDatetime"] = "2024-12-27 21:26:57"
    response = client.put(f"/tasks/{task_id}", json=updated_task, headers=user2_header)
    resp = response.json()
    assert resp["title"] == updated_task["title"]
    assert resp["content"] == updated_task["content"]
    assert resp["startDatetime"] == updated_task["startDatetime"]
    assert resp["endDatetime"] == updated_task["endDatetime"]

    assert response.status_code == 200


def test_delete_task(user1_header, task):
    task_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.delete(f"/tasks/{task_id}", headers=user1_header)
    assert response.status_code == 204

    response = client.get("/tasks", headers=user1_header)
    assert response.status_code == 200

    resp = response.json()
    assert isinstance(resp, list)
    assert len(resp) == (USER001_SEED_DATA_SIZE - 1)


def test_mark_task_as_done(user2_header, task):
    task_id = "123e4567-e89b-12d3-a456-426614174002"
    response = client.put(f"/tasks/{task_id}/done", headers=user2_header)
    assert response.status_code == 200

    resp = response.json()
    assert resp["done"] == True


def test_unmark_task_as_done(user2_header, task):
    task_id = "123e4567-e89b-12d3-a456-426614174002"
    response = client.delete(f"/tasks/{task_id}/done", headers=user2_header)
    assert response.status_code == 200

    resp = response.json()
    assert resp["done"] == False
