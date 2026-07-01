
from pydantic import BaseModel


class RoleMenuAuth(BaseModel):
    role_id: int
    menu_ids: list[int]


class RoleMenuResponse(BaseModel):
    role_id: int
    menu_ids: list[int]
