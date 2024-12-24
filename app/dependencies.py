from typing import Annotated

from fastapi import Depends

from core.security import get_authorized_user
from schemas.user import User
from services.task import TaskService

UserDep = Annotated[User, Depends(get_authorized_user)]
TaskServiceDep = Annotated[TaskService, Depends(TaskService)]
