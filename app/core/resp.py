from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar('T')

# 1. 定义纯粹的分页数据结构
# 它不包含 code 和 msg，只包含分页核心数据
class PageInfo(BaseModel, Generic[T]):
    items: List[T] = Field(description="数据列表")
    total: int = Field(description="总条数")
    page: int = Field(default=1, description="当前页")
    size: int = Field(default=10, description="页大小")
    pages: int = Field(description="总页数")

# 2. 定义统一响应外壳
class Result(BaseModel, Generic[T]):
    code: int = Field(default=0, description="业务状态码")
    msg: str = Field(default="success", description="提示信息")
    data: Optional[T] = Field(default=None, description="数据主体")

    model_config = ConfigDict(populate_by_name=True)

    @property
    def is_success(self) -> bool:
        return self.code == 0

    @classmethod
    def success(cls, data: Optional[T] = None) -> "Result[T]":
        return cls(code=0, msg="success", data=data)

    @classmethod
    def error(cls, code: int = 500, msg: str = "Error", data: Any = None) -> "Result[T]":
        return cls(code=code, msg=msg, data=data)

    # 3. 专门为分页提供一个快捷构造方法
    # 返回类型注解明确为 Result[PageInfo[T]]
    @classmethod
    def success_page(cls, items: List[T], total: int, page: int = 1, size: int = 10) -> "Result[PageInfo[T]]":
        pages = (total + size - 1) // size if size > 0 else 0
        page_info = PageInfo[T](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        return cls(code=0, msg="success", data=page_info)
