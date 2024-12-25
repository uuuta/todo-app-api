from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from models.task import Task


class TaskDBClient(ABC):

    @abstractmethod
    def create_task(self, task: Task) -> Task:
        pass

    @abstractmethod
    def get_task_list(self, user_id: str) -> List[Task]:
        pass

    @abstractmethod
    def get_task_by_id(self, user_id: str, task_id: UUID) -> Task | None:
        pass

    @abstractmethod
    def update_task(self, task: Task) -> Task | None:
        pass

    @abstractmethod
    def delete_task(self, user_id: str, task_id: UUID) -> None:
        pass
