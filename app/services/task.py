from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from fastapi import HTTPException

from config import settings
from core.logging import get_logger
from database.database import TaskDatabaseDep
from models.task import Task as TaskModel
from schemas.task import TaskCreateRequest, TaskResponse

logger = get_logger()


class TaskService:
    def __init__(self, task_db: TaskDatabaseDep):
        self.task_db = task_db

    def create_task(self, user_id: str, task_req: TaskCreateRequest) -> TaskResponse:
        task_model = TaskModel(user_id=user_id, task_id=uuid4(),
                               registration_datetime=datetime.now(ZoneInfo(settings.timezone)).strftime(
                                   "%Y-%m-%d %H:%M:%S"), **task_req.model_dump())
        created_task = self.task_db.create_task(task_model)
        return TaskResponse(task_id=created_task.task_id, **created_task.model_dump())

    def get_task_list(self, user_id: str) -> List[TaskResponse]:
        got_task_model_list = self.task_db.get_task_list(user_id)
        tasks = [TaskResponse(task_id=task_model.task_id, **task_model.model_dump())
                 for task_model in got_task_model_list]
        return sorted(tasks, key=lambda x: x.registration_datetime, reverse=True)

    def get_task(self, user_id: str, task_id: UUID) -> TaskResponse:
        got_task_model = self.task_db.get_task_by_id(user_id, task_id)
        if got_task_model is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return TaskResponse(task_id=got_task_model.task_id, **got_task_model.model_dump())

    def update_task(self, user_id: str, task_id: UUID, task_req: TaskCreateRequest) -> TaskResponse:
        task_model = TaskModel(user_id=user_id, task_id=task_id, **task_req.model_dump())
        updated_task = self.task_db.update_task(task_model)
        if updated_task is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return TaskResponse(task_id=updated_task.task_id, **updated_task.model_dump())

    def delete_task(self, user_id: str, task_id: UUID) -> None:
        self.task_db.delete_task(user_id, task_id)
        return

    def mark_task_as_done(self, user_id: str, task_id: UUID) -> TaskResponse:
        updated_task = self.task_db.update_done_flg(user_id, task_id, True)
        return TaskResponse(task_id=updated_task.task_id, **updated_task.model_dump())

    def unmark_task_as_done(self, user_id: str, task_id: UUID) -> TaskResponse:
        updated_task = self.task_db.update_done_flg(user_id, task_id, False)
        return TaskResponse(task_id=updated_task.task_id, **updated_task.model_dump())
