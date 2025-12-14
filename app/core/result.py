from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar('T')


class Result(BaseModel, Generic[T]):
    """统一响应结构"""
    code: int = 0
    msg: str = "success"
    data: Optional[T] = None

    @classmethod
    def success(cls, data: Optional[T] = None) -> "Result[T]":
        """成功响应"""
        return cls(code=0, msg="success", data=data)

    @classmethod
    def error(cls, code: int = 500, msg: str = "Internal Server Error") -> "Result[Any]":
        """错误响应"""
        return cls(code=code, msg=msg, data=None)

    @classmethod
    def error_with_data(cls, code: int = 500, msg: str = "Internal Server Error", data: Optional[Any] = None) -> "Result[Any]":
        """带数据的错误响应"""
        return cls(code=code, msg=msg, data=data)


class PageResult(BaseModel, Generic[T]):
    """分页响应结构"""
    code: int = 0
    msg: str = "success"
    data: Optional[dict] = None

    @classmethod
    def success(cls, items: list, total: int, page: int = 1, size: int = 10) -> "PageResult[T]":
        """成功分页响应"""
        return cls(
            code=0,
            msg="success",
            data={
                "items": items,
                "total": total,
                "page": page,
                "size": size,
                "pages": (total + size - 1) // size
            }
        )
