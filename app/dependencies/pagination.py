from fastapi import Query,Depends
from pydantic import BaseModel, Field
from typing import Annotated

class PageParams(BaseModel):
    page: int = Field(default=1, ge=1, description="页码，从 1 开始")
    size: int = Field(default=10, ge=1, le=100, description="每页数量，最大 100")

def get_page_params(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
):
    return PageParams(page=page, size=size)

PageDep = Annotated[PageParams, Depends(get_page_params)]
