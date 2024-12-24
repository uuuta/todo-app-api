from fastapi import Request, HTTPException
# from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from schemas.error import ErrorResponse


# pydanticによるリクエストのバリデーションエラーをカスタマイズする場合にコメントアウト
# async def validation_exception_handler(request: Request, exc: RequestValidationError) \
#         -> JSONResponse:
#     print("validation_exception_handler")
#     error_response = ErrorResponse(message="Invalid request", detail=exc.errors())
#     return JSONResponse(
#         status_code=HTTP_422_UNPROCESSABLE_ENTITY,
#         content=error_response.model_dump()
#     )


async def http_exception_handler(request: Request, exc: HTTPException) \
        -> JSONResponse:
    error_response = ErrorResponse(message=exc.detail, detail=[])
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )
