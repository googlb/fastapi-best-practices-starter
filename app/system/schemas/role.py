from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RoleBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    status: int = 1


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None


class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    menu_ids: Optional[List[int]] = None
    
    class Config:
        from_attributes = True
