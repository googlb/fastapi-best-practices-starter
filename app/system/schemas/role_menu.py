from pydantic import BaseModel
from typing import List


class RoleMenuAuth(BaseModel):
    role_id: int
    menu_ids: List[int]


class RoleMenuResponse(BaseModel):
    role_id: int
    menu_ids: List[int]

