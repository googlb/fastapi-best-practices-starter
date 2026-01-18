"""
全局异常处理模块

提供统一的异常处理机制，包括：
1. 自定义业务异常类
2. HTTP 异常处理器
3. 参数校验异常处理器
4. 业务异常处理器
"""
from typing import Any
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.resp import Result


# ========================================
# 自定义异常类
# ========================================

class BusinessException(Exception):
    """
    业务异常基类
    
    所有业务逻辑异常都应继承此类，而不是直接抛出 Exception。
    这样可以在全局异常处理器中统一捕获并转换为标准的 Result 格式。
    """
    def __init__(self, code: int, msg: str, data: Any = None) -> None:
        self.code = code
        self.msg = msg
        self.data = data
        super().__init__(msg)


class AuthenticationException(BusinessException):
    """认证异常 (401)"""
    def __init__(self, msg: str = "认证失败", data: Any = None) -> None:
        super().__init__(code=401, msg=msg, data=data)


class PermissionException(BusinessException):
    """权限异常 (403)"""
    def __init__(self, msg: str = "权限不足", data: Any = None) -> None:
        super().__init__(code=403, msg=msg, data=data)


class NotFoundException(BusinessException):
    """资源不存在异常 (404)"""
    def __init__(self, msg: str = "资源不存在", data: Any = None) -> None:
        super().__init__(code=404, msg=msg, data=data)


class ValidationException(BusinessException):
    """业务验证异常 (400)"""
    def __init__(self, msg: str = "参数验证失败", data: Any = None) -> None:
        super().__init__(code=400, msg=msg, data=data)


class ServerException(BusinessException):
    """服务器内部异常 (500)"""
    def __init__(self, msg: str = "服务器内部错误", data: Any = None) -> None:
        super().__init__(code=500, msg=msg, data=data)


# ========================================
# 异常处理器
# ========================================

async def http_exception_handler(
    request: Request, 
    exc: StarletteHTTPException
) -> JSONResponse:
    """
    拦截 HTTP 异常 (如 404, 401) 并转为统一 JSON 格式
    
    注意：这里保持 HTTP 状态码与业务 code 一致
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=Result.error(
            code=exc.status_code, 
            msg=exc.detail
        ).model_dump()
    )


async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError
) -> JSONResponse:
    """
    拦截参数校验错误 (422)
    
    将 Pydantic 验证错误转换为统一的 Result 格式
    """
    return JSONResponse(
        status_code=422,
        content=Result.error(
            code=422, 
            msg="参数校验错误", 
            data=exc.errors()
        ).model_dump()
    )


async def business_exception_handler(
    request: Request, 
    exc: BusinessException
) -> JSONResponse:
    """
    统一处理业务异常
    
    业务异常使用 HTTP 200，通过 code 字段区分错误类型。
    这样前端可以统一处理响应格式，不需要根据 HTTP 状态码做特殊处理。
    
    如果需要使用 HTTP 状态码区分错误，可以改为：
    status_code=exc.code if exc.code >= 400 else 200
    """
    return JSONResponse(
        status_code=200,  # 业务异常统一返回 200
        content=Result.error(
            code=exc.code,
            msg=exc.msg,
            data=exc.data
        ).model_dump()
    )
