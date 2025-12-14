from pydantic import BaseModel, UUID4
from typing import Optional


class DictBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    status: int = 1


class DictCreate(DictBase):
    pass


class DictUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None


class DictResponse(DictBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DictDataBase(BaseModel):
    dict_id: UUID4
    label: str
    value: str
    sort: int = 0
    is_default: bool = False
    status: int = 1


class DictDataCreate(DictDataBase):
    pass


class DictDataUpdate(BaseModel):
    dict_id: Optional[UUID4] = None
    label: Optional[str] = None
    value: Optional[str] = None
    sort: Optional[int] = None
    is_default: Optional[bool] = None
    status: Optional[int] = None


class DictDataResponse(DictDataBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
