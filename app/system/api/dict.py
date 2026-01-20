from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies.database import get_session as get_db
from app.dependencies.pagination import PageDep
from app.system.crud.crud_dict import crud_dict
from app.system.crud.crud_dict_data import crud_dict_data
from app.core.resp import Result, PageInfo
from app.system.schemas.dict import (
    DictCreate,
    DictUpdate,
    DictResponse,
    DictDataCreate,
    DictDataUpdate,
    DictDataResponse
)

router = APIRouter()


@router.get("", response_model=Result[PageInfo[DictResponse]])
async def get_dicts(
    pagination: PageDep,
    session: AsyncSession = Depends(get_db)
) -> Result[PageInfo[DictResponse]]:
    """获取字典列表"""
    dicts, total = await crud_dict.get_page(
        session, page=pagination.page, page_size=pagination.size
    )
    return Result.success_page(dicts, total, pagination.page, pagination.size)


@router.get("/{dict_id}", response_model=Result[DictResponse])
async def get_dict(
    dict_id: int,
    session: AsyncSession = Depends(get_db)
) -> Result[DictResponse]:
    """获取字典详情"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")
    return Result.success(dict_item)


@router.get("/code/{dict_code}", response_model=Result)
async def get_dict_by_code(
    dict_code: str,
    session: AsyncSession = Depends(get_db)
) -> Result:
    """根据编码获取字典"""
    dict_item = await crud_dict.get_by_code(session, dict_code)
    if not dict_item:
        return Result.error(404, "Dict not found")

    # 获取字典数据
    dict_data_list = await crud_dict_data.get_by_dict_id(session, dict_item.id)

    # 创建一个新的字典对象，包含数据列表
    # 注意：这里返回的结构比较特殊，可能需要定义专门的 Schema，这里暂时保持 Result 泛型
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


@router.get("/{dict_id}/data", response_model=Result[PageInfo[DictDataResponse]])
async def get_dict_data(
    dict_id: int,
    pagination: PageDep,
    session: AsyncSession = Depends(get_db)
) -> Result[PageInfo[DictDataResponse]]:
    """获取字典数据列表"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")

    dict_data_list, total = await crud_dict_data.get_page(
        session, dict_id=dict_id, page=pagination.page, page_size=pagination.size
    )
    return Result.success_page(dict_data_list, total, pagination.page, pagination.size)


@router.post("/", response_model=Result[DictResponse])
async def create_dict(
    dict_in: DictCreate,
    session: AsyncSession = Depends(get_db)
) -> Result[DictResponse]:
    """创建字典"""
    dict_item = await crud_dict.create(session, obj_in=dict_in)
    return Result.success(dict_item)


@router.put("/{dict_id}", response_model=Result[DictResponse])
async def update_dict(
    dict_id: int,
    dict_in: DictUpdate,
    session: AsyncSession = Depends(get_db)
) -> Result[DictResponse]:
    """更新字典"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")

    dict_item = await crud_dict.update(session, db_obj=dict_item, obj_in=dict_in)
    return Result.success(dict_item)


@router.delete("/{dict_id}", response_model=Result[str])
async def delete_dict(
    dict_id: int,
    session: AsyncSession = Depends(get_db)
) -> Result[str]:
    """删除字典"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")

    await crud_dict.delete(session, id=dict_id)
    return Result.success("Dict deleted successfully")


@router.post("/{dict_id}/data", response_model=Result[DictDataResponse])
async def create_dict_data(
    dict_id: int,
    data_in: DictDataCreate,
    session: AsyncSession = Depends(get_db)
) -> Result[DictDataResponse]:
    """创建字典数据"""
    dict_item = await crud_dict.get(session, dict_id)
    if not dict_item:
        return Result.error(404, "Dict not found")

    # 强制覆盖 dict_id
    data_dict = data_in.model_dump()
    data_dict["dict_id"] = dict_id
    # 因为 DictDataCreate 对应的模型是 DictDataCreate，我们这里转成了 dict
    # crud create 接受 CreateSchemaType | dict
    # 我们需要重新构造一个 CreateSchemaType 或者直接传 dict (如果 crud 支持)
    # CRUDBase.create(..., obj_in: CreateSchemaType)
    # 所以我们需要把 dict 转回 model，或者修改 data_in 对象
    
    # 更好的方式：
    data_in.dict_id = dict_id
    dict_data = await crud_dict_data.create(session, obj_in=data_in)
    return Result.success(dict_data)


@router.put("/data/{data_id}", response_model=Result[DictDataResponse])
async def update_dict_data(
    data_id: int,
    data_in: DictDataUpdate,
    session: AsyncSession = Depends(get_db)
) -> Result[DictDataResponse]:
    """更新字典数据"""
    dict_data = await crud_dict_data.get(session, data_id)
    if not dict_data:
        return Result.error(404, "Dict data not found")

    dict_data = await crud_dict_data.update(session, db_obj=dict_data, obj_in=data_in)
    return Result.success(dict_data)


@router.delete("/data/{data_id}", response_model=Result[str])
async def delete_dict_data(
    data_id: int,
    session: AsyncSession = Depends(get_db)
) -> Result[str]:
    """删除字典数据"""
    dict_data = await crud_dict_data.get(session, data_id)
    if not dict_data:
        return Result.error(404, "Dict data not found")

    await crud_dict_data.delete(session, id=data_id)
    return Result.success("Dict data deleted successfully")
