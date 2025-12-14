from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.resp import Result

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """拦截 HTTP 异常 (如 404, 401) 并转为统一 JSON 格式"""
    return JSONResponse(
        status_code=exc.status_code, # 保持 HTTP 状态码（如 401）
        content=Result.error(code=exc.status_code, msg=exc.detail).model_dump_json()
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """拦截参数校验错误 (422)"""
    return JSONResponse(
        status_code=422,
        content=Result.error(code=422, msg="参数校验错误", data=exc.errors()).model_dump_json()
    )
