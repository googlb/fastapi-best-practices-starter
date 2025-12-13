# This file will contain the CRUD operations for the News model.
# (Create, Read, Update, Delete)
from sqlmodel import Session, select

from .models import News
from .schemas import NewsCreate, NewsUpdate


def create_news(*, session: Session, news_in: NewsCreate) -> News:
    ...

def get_news_by_id(*, session: Session, news_id: int) -> News | None:
    ...

def update_news(*, session: Session, news_id: int, news_in: NewsUpdate) -> News | None:
    ...

def delete_news(*, session: Session, news_id: int) -> None:
    ...
