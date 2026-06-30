from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.resp import PageInfo, Result
from app.dependencies.database import get_session as get_db
from app.dependencies.pagination import PageDep
from app.system.crud.crud_dict import crud_dict
from app.system.crud.crud_dict_data import crud_dict_data
from app.system.schemas.dict import (
    DictCreate,
    DictDataCreate,
    DictDataResponse,
    DictDataUpdate,
    DictResponse,
    DictUpdate,
)
from app.system.services.dict_service import sys_dict_service

router = APIRouter()


@router.get("", response_model=Result[PageInfo[DictResponse]])
async def get_dicts(
    pagination: PageDep, session: AsyncSession = Depends(get_db)
) -> Result[PageInfo[DictResponse]]:
    """获取字典列表"""
    dicts, total = await crud_dict.get_page(
        session, page=pagination.page, page_size=pagination.size
    )
    return Result.success_page(dicts, total, pagination.page, pagination.size)


@router.get("/{dict_id}", response_model=Result[DictResponse])
async def get_dict(
    dict_id: int, session: AsyncSession = Depends(get_db)
) -> Result[DictResponse]:
    """获取字典详情"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "字典不存在")
    return Result.success(dict_item)


@router.get("/code/{dict_code}", response_model=Result)
async def get_dict_by_code(
    dict_code: str, session: AsyncSession = Depends(get_db)
) -> Result:
    """根据编码获取字典"""
    result = await sys_dict_service.get_dict_by_code(session, dict_code)
    if not result:
        return Result.error(404, "字典不存在")
    return Result.success(result)


@router.get("/{dict_id}/data", response_model=Result[PageInfo[DictDataResponse]])
async def get_dict_data(
    dict_id: int, pagination: PageDep, session: AsyncSession = Depends(get_db)
) -> Result[PageInfo[DictDataResponse]]:
    """获取字典数据列表"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "字典不存在")

    dict_data_list, total = await crud_dict_data.get_page(
        session, dict_id=dict_id, page=pagination.page, page_size=pagination.size
    )
    return Result.success_page(dict_data_list, total, pagination.page, pagination.size)


@router.post("/", response_model=Result[DictResponse])
async def create_dict(
    dict_in: DictCreate, session: AsyncSession = Depends(get_db)
) -> Result[DictResponse]:
    """创建字典"""
    dict_item = await sys_dict_service.create_dict(session, dict_in)
    return Result.success(dict_item)


@router.put("/{dict_id}", response_model=Result[DictResponse])
async def update_dict(
    dict_id: int, dict_in: DictUpdate, session: AsyncSession = Depends(get_db)
) -> Result[DictResponse]:
    """更新字典"""
    dict_item = await sys_dict_service.update_dict(session, dict_id, dict_in)
    return Result.success(dict_item)


@router.delete("/{dict_id}", response_model=Result[str])
async def delete_dict(
    dict_id: int, session: AsyncSession = Depends(get_db)
) -> Result[str]:
    """删除字典"""
    await sys_dict_service.delete_dict(session, dict_id)
    return Result.success("字典删除成功")


@router.post("/{dict_id}/data", response_model=Result[DictDataResponse])
async def create_dict_data(
    dict_id: int, data_in: DictDataCreate, session: AsyncSession = Depends(get_db)
) -> Result[DictDataResponse]:
    """创建字典数据"""
    dict_data = await sys_dict_service.create_dict_data(session, dict_id, data_in)
    return Result.success(dict_data)


@router.put("/data/{data_id}", response_model=Result[DictDataResponse])
async def update_dict_data(
    data_id: int, data_in: DictDataUpdate, session: AsyncSession = Depends(get_db)
) -> Result[DictDataResponse]:
    """更新字典数据"""
    dict_data = await sys_dict_service.update_dict_data(session, data_id, data_in)
    return Result.success(dict_data)


@router.delete("/data/{data_id}", response_model=Result[str])
async def delete_dict_data(
    data_id: int, session: AsyncSession = Depends(get_db)
) -> Result[str]:
    """删除字典数据"""
    await sys_dict_service.delete_dict_data(session, data_id)
    return Result.success("字典数据删除成功")
