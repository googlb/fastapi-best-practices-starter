from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pydantic import BaseModel, ConfigDict

# 定义北京时区
SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")

def format_datetime(dt: datetime) -> str:
    """全局时间格式化函数"""
    if dt is None:
        return None
    # 补全 UTC 时区
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    # 转为北京时间并格式化
    return dt.astimezone(SHANGHAI_TZ).strftime("%Y-%m-%d %H:%M:%S")

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        # ✅ 核心配置：类似 FastJSON 的全局类型转换
        # 只要 Schema 里有 datetime 类型的字段，都会走这个逻辑
        json_encoders={
            datetime: format_datetime
        }
    )
