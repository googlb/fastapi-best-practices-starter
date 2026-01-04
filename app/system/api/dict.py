from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.dependencies.database import get_session as get_db
from app.system.crud.crud_dict import crud_dict
from app.system.crud.crud_dict_data import crud_dict_data
from app.core.resp import Result

router = APIRouter()


@router.get("")
async def get_dicts(
    page: int = 1,
    size: int = 20,
    session: AsyncSession = Depends(get_db)
):
    """获取字典列表"""
    dicts, total = await crud_dict.get_page(session, page=page, page_size=size)
    return Result.success_page(dicts, total, page, size)


@router.get("/{dict_id}")
async def get_dict(
    dict_id: int,
    session: AsyncSession = Depends(get_db)
):
    """获取字典详情"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")
    return Result.success(dict_item)


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

    # 创建一个新的字典对象，包含数据列表
    result = {
        "id": dict_item.id,
        "name": dict_item.name,
        "code": dict_item.code,
        "description": dict_item.description,
        "created_at": dict_item.created_at,
        "updated_at": dict_item.updated_at,
        "data": dict_data_list
    }
    return Result.success(result)


@router.get("/{dict_id}/data")
async def get_dict_data(
    dict_id: int,
    page: int = 1,
    size: int = 20,
    session: AsyncSession = Depends(get_db)
):
    """获取字典数据列表"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")

    dict_data_list, total = await crud_dict_data.get_page(session, dict_id=dict_id, page=page, page_size=size)
    return Result.success_page(dict_data_list, total, page, size)


@router.post("/")
async def create_dict(
    dict_data: dict,
    session: AsyncSession = Depends(get_db)
):
    """创建字典"""
    dict_item = await crud_dict.create(session, dict_data)
    return Result.success(dict_item)


@router.put("/{dict_id}")
async def update_dict(
    dict_id: int,
    dict_data: dict,
    session: AsyncSession = Depends(get_db)
):
    """更新字典"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")

    dict_item = await crud_dict.update(session, dict_item, dict_data)
    return Result.success(dict_item)


@router.delete("/{dict_id}")
async def delete_dict(
    dict_id: int,
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
    dict_id: int,
    data_item: dict,
    session: AsyncSession = Depends(get_db)
):
    """创建字典数据"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")

    data_item["dict_id"] = dict_id
    dict_data = await crud_dict_data.create(session, data_item)
    return Result.success(dict_data)


@router.put("/data/{data_id}")
async def update_dict_data(
    data_id: int,
    data_item: dict,
    session: AsyncSession = Depends(get_db)
):
    """更新字典数据"""
    dict_data = await crud_dict_data.get(session, data_id)
    if not dict_data:
        return Result.error(404, "Dict data not found")

    dict_data = await crud_dict_data.update(session, dict_data, data_item)
    return Result.success(dict_data)


@router.delete("/data/{data_id}")
async def delete_dict_data(
    data_id: int,
    session: AsyncSession = Depends(get_db)
):
    """删除字典数据"""
    dict_data = await crud_dict_data.get(session, data_id)
    if not dict_data:
        return Result.error(404, "Dict data not found")

    await crud_dict_data.delete(session, data_id)
    return Result.success({"message": "Dict data deleted successfully"})
