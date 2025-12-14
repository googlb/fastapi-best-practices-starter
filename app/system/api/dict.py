from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.dependencies.database import get_session as get_db
from app.system.models import SysDict, SysDictData
from app.system.crud.crud_dict import crud_dict
from app.system.crud.crud_dict_data import crud_dict_data
from app.core.result import Result, PageResult

router = APIRouter()


@router.get("/")
async def get_dicts(
    page: int = 1,
    size: int = 20,
    session: AsyncSession = Depends(get_db)
):
    """获取字典列表"""
    skip = (page - 1) * size
    dicts, total = await crud_dict.get_page(session, skip=skip, limit=size)
    return PageResult.success([dict_item.model_dump() for dict_item in dicts], total, page, size)


@router.get("/{dict_id}")
async def get_dict(
    dict_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    """获取字典详情"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")
    return Result.success(dict_item.model_dump())


@router.get("/code/{dict_code}")
async def get_dict_by_code(
    dict_code: str,
    session: AsyncSession = Depends(get_db)
):
    """根据编码获取字典"""
    dict_item = await crud_dict.get_by_code(session, dict_code)
    if not dict_item:
        return Result.error(404, "Dict not found")
    
    # 获取字典数据
    dict_data_list = await crud_dict_data.get_by_dict_id(session, dict_item.id)
    
    result = dict_item.model_dump()
    result["data"] = [data.model_dump() for data in dict_data_list]
    return Result.success(result)


@router.get("/{dict_id}/data")
async def get_dict_data(
    dict_id: UUID,
    page: int = 1,
    size: int = 20,
    session: AsyncSession = Depends(get_db)
):
    """获取字典数据列表"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")
    
    skip = (page - 1) * size
    dict_data_list = await crud_dict_data.get_by_dict_id(session, dict_id, skip=skip, limit=size)
    total = await crud_dict_data.count_by_dict_id(session, dict_id)
    return PageResult.success([data.model_dump() for data in dict_data_list], total, page, size)


@router.post("/")
async def create_dict(
    dict_data: dict,
    session: AsyncSession = Depends(get_db)
):
    """创建字典"""
    dict_item = await crud_dict.create(session, dict_data)
    return Result.success(dict_item.model_dump())


@router.put("/{dict_id}")
async def update_dict(
    dict_id: UUID,
    dict_data: dict,
    session: AsyncSession = Depends(get_db)
):
    """更新字典"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")
    
    dict_item = await crud_dict.update(session, dict_item, dict_data)
    return Result.success(dict_item.model_dump())


@router.delete("/{dict_id}")
async def delete_dict(
    dict_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    """删除字典"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")
    
    await crud_dict.delete(session, dict_id)
    return Result.success({"message": "Dict deleted successfully"})


@router.post("/{dict_id}/data")
async def create_dict_data(
    dict_id: UUID,
    data_item: dict,
    session: AsyncSession = Depends(get_db)
):
    """创建字典数据"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")
    
    data_item["dict_id"] = dict_id
    dict_data = await crud_dict_data.create(session, data_item)
    return Result.success(dict_data.model_dump())


@router.put("/data/{data_id}")
async def update_dict_data(
    data_id: UUID,
    data_item: dict,
    session: AsyncSession = Depends(get_db)
):
    """更新字典数据"""
    dict_data = await crud_dict_data.get(session, data_id)
    if not dict_data:
        return Result.error(404, "Dict data not found")
    
    dict_data = await crud_dict_data.update(session, dict_data, data_item)
    return Result.success(dict_data.model_dump())


@router.delete("/data/{data_id}")
async def delete_dict_data(
    data_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    """删除字典数据"""
    dict_data = await crud_dict_data.get(session, data_id)
    if not dict_data:
        return Result.error(404, "Dict data not found")
    
    await crud_dict_data.delete(session, data_id)
    return Result.success({"message": "Dict data deleted successfully"})
