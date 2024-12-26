from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aws_region: str = "ap-northeast-1"
    dynamodb_task_table_name: str = "tasks"
    dynamodb_endpoint: Optional[str] = None
    environment: str = "aws-lambda"
    log_level: str = "INFO"
    log_level_default: str = "INFO"
    timezone: str = "Asia/Tokyo"

    class Config:
        env_prefix = "APP_"
        env_file = ".env"
        extra = "ignore"


settings = Settings()
app_config = {
    "title": "TODO Application API",
    "description": "This application is an API example for TODO application.",
    "version": "0.1.0"
}
