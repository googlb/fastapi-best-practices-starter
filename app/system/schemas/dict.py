from datetime import datetime

from pydantic import BaseModel


class DictBase(BaseModel):
    name: str
    code: str
    description: str | None = None
    status: int = 1


class DictCreate(DictBase):
    pass


class DictUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    description: str | None = None
    status: int | None = None


class DictResponse(DictBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DictDataBase(BaseModel):
    dict_id: int
    label: str
    value: str
    sort: int = 0
    is_default: bool = False
    status: int = 1


class DictDataCreate(DictDataBase):
    pass


class DictDataUpdate(BaseModel):
    dict_id: int | None = None
    label: str | None = None
    value: str | None = None
    sort: int | None = None
    is_default: bool | None = None
    status: int | None = None


class DictDataResponse(DictDataBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
