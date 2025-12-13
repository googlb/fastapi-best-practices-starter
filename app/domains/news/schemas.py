from typing import Optional
from sqlmodel import SQLModel


class NewsBase(SQLModel):
    title: str
    content: str


class NewsCreate(NewsBase):
    pass


class NewsRead(NewsBase):
    id: int


class NewsUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
