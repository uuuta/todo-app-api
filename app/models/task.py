from uuid import UUID

from pydantic import BaseModel, Field, AliasChoices


class Task(BaseModel):
    user_id: str = \
        Field(description="Partition Key", serialization_alias="userId",
              validation_alias=AliasChoices('user_id', 'userId'), exclude=True)
    task_id: UUID = \
        Field(description="Sort Key", serialization_alias="taskId",
              validation_alias=AliasChoices('task_id', 'taskId'), exclude=True)
    title: str
    content: str | None = None
    registration_datetime: str = \
        Field(None, serialization_alias="registrationDatetime",
              validation_alias=AliasChoices('registration_datetime', 'registrationDatetime'))
    start_datetime: str | None = \
        Field(None, serialization_alias="startDatetime",
              validation_alias=AliasChoices('start_datetime', 'startDatetime'))
    end_datetime: str | None = \
        Field(None, serialization_alias="endDatetime",
              validation_alias=AliasChoices('end_datetime', 'endDatetime'))
    done: bool = Field(False)
