from typing import List
from uuid import UUID

from fastapi import APIRouter

from core.logging import get_logger
from dependencies import UserDep, TaskServiceDep
from schemas.error import ErrorResponse
from schemas.task import TaskCreateRequest, TaskResponse

logger = get_logger(__name__)
router = APIRouter()


@router.post("/tasks",
             description="新規にタスクを作成します。",
             response_model=TaskResponse,
             status_code=201,
             responses={403: {"description": "Forbidden", "model": ErrorResponse}})
def create_task(user: UserDep, task_req: TaskCreateRequest, task_service: TaskServiceDep):
    logger.info(f"userId={user.id}")
    return task_service.create_task(user.id, task_req)


@router.get("/tasks",
            description="タスクリストを取得します。リストは登録日時の降順です。",
            response_model=List[TaskResponse],
            responses={403: {"description": "Forbidden", "model": ErrorResponse}})
def list_tasks(user: UserDep, task_service: TaskServiceDep):
    logger.info(f"userId={user.id}")
    return task_service.get_task_list(user.id)


@router.get("/tasks/{task_id}",
            description="タスクを取得します。",
            response_model=TaskResponse,
            responses={403: {"description": "Forbidden", "model": ErrorResponse},
                       404: {"description": "Not Found", "model": ErrorResponse}})
def get_task(user: UserDep, task_id: UUID, task_service: TaskServiceDep):
    logger.info(f"userId={user.id} taskId={task_id}")
    return task_service.get_task(user.id, task_id)


@router.put("/tasks/{task_id}",
            description="タスクを更新します。",
            response_model=TaskResponse,
            responses={403: {"description": "Forbidden", "model": ErrorResponse},
                       404: {"description": "Not Found", "model": ErrorResponse}})
def update_task(user: UserDep, task_id: UUID, task_req: TaskCreateRequest, task_service: TaskServiceDep):
    logger.info(f"userId={user.id} taskId={task_id}")
    return task_service.update_task(user.id, task_id, task_req)


@router.delete("/tasks/{task_id}",
               description="タスクを削除します。",
               status_code=204,
               responses={403: {"description": "Forbidden", "model": ErrorResponse}})
def delete_task(user: UserDep, task_id: UUID, task_service: TaskServiceDep):
    logger.info(f"userId={user.id} taskId={task_id}")
    task_service.delete_task(user.id, task_id)


@router.put("/tasks/{task_id}/done",
            description="タスクを完了にします。",
            response_model=TaskResponse,
            responses={403: {"description": "Forbidden", "model": ErrorResponse}})
def mark_task_as_done(user: UserDep, task_id: UUID, task_service: TaskServiceDep):
    logger.info(f"userId={user.id} taskId={task_id}")
    return task_service.mark_task_as_done(user.id, task_id)


@router.delete("/tasks/{task_id}/done",
               description="タスクを未完了にします。",
               response_model=TaskResponse,
               responses={403: {"description": "Forbidden", "model": ErrorResponse}})
def unmark_task_as_done(user: UserDep, task_id: UUID, task_service: TaskServiceDep):
    logger.info(f"userId={user.id} taskId={task_id}")
    return task_service.unmark_task_as_done(user.id, task_id)
