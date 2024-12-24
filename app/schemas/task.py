from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, PlainSerializer

CustomDatetime = Annotated[
    datetime,
    PlainSerializer(lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S"))
]


class TaskBase(BaseModel):
    title: str = \
        Field(description="タイトル", examples=["ブログを書く"], min_length=1, max_length=100)
    content: str | None = \
        Field(None, description="内容", max_length=1000,
              examples=["最近流行っているフレームワークを調べてブログ記事にする"])


class TaskCreateRequest(TaskBase):
    start_datetime: CustomDatetime | None = \
        Field(None, description="タスクの開始 %Y-%m-%d %H:%M:%S形式で指定する",
              validation_alias="startDatetime",
              examples=["2023-12-18 09:00:00"])
    end_datetime: CustomDatetime | None = \
        Field(None, description="タスクの期限 %Y-%m-%d %H:%M:%S形式で指定する",
              validation_alias="endDatetime",
              examples=["2023-12-19 09:00:00"])
    pass


class TaskResponse(TaskBase):
    task_id: UUID = Field(description="UUID形式のタスクID",
                          serialization_alias="taskId",
                          examples=["389a5bb4-5fe5-47e5-972a-7bf3da3543f1"])
    registration_datetime: CustomDatetime | None = \
        Field(None, description="タスクの登録日時 %Y-%m-%d %H:%M:%S形式で指定する",
              serialization_alias="registrationDatetime",
              examples=["2023-12-18 08:00:00"])
    start_datetime: CustomDatetime | None = \
        Field(None, description="タスクの開始 %Y-%m-%d %H:%M:%S形式で指定する",
              serialization_alias="startDatetime",
              examples=["2023-12-18 09:00:00"])
    end_datetime: CustomDatetime | None = \
        Field(None, description="タスクの期限 %Y-%m-%d %H:%M:%S形式で指定する",
              serialization_alias="endDatetime",
              examples=["2023-12-19 09:00:00"])
    done: bool = Field(False, description="完了フラグ", examples=[True])
