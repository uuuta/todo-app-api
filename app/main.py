import uvicorn
from fastapi import FastAPI, HTTPException
# from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from config import app_config, settings
from core.handler import http_exception_handler
from core.logging import get_logger
from routers import task

logger = get_logger()
logger.info(app_config)
logger.info(settings)

app = FastAPI(**app_config)
app.add_middleware(
    CORSMiddleware,
    # 許可するオリジンを指定
    allow_origins=["*"],
    # cookieの共有を行う設定（defaultはFalse）
    allow_credentials=True,
    # 許可するHTTPメソッドを指定（defaultはGET）
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    # オリジン間リクエストで許可するHTTPヘッダーを指定
    # Accept、Accept-Language、Content-Language、Content-Typeヘッダーが常に許可
    allow_headers=["*"],
)

app.include_router(task.router)
# pydanticによるリクエストのバリデーションエラーをカスタマイズする場合にコメントアウト
# app.add_exception_handler(RequestValidationError, handler.validation_exception_handler)
app.add_exception_handler(HTTPException, handler=http_exception_handler)

handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
