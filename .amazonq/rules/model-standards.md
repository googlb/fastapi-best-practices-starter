# SQLModel 建表规范

## 表级注释
- 每个 SQLModel 类必须有 docstring，格式：`"""表名 - 功能描述"""`
- 示例：`"""用户表 - 后台系统用户管理"""`

## 字段级注释
- 每个字段必须在 Field 中添加 `description` 参数
- 格式：`Field(..., description="中文字段说明")`
- 示例：`username: str = Field(unique=True, index=True, description="用户名")`

## 标准字段
所有表都应包含以下标准字段：
- `id: Optional[int]` - 主键，自增
- `created_at: datetime` - 创建时间，默认 `datetime.utcnow`
- `updated_at: datetime` - 更新时间，默认 `datetime.utcnow`

## 字段必填性原则
- 业务必需字段：无默认值，必填
- 状态字段：设置合理默认值（如 `is_active=True`）
- 可选信息：使用 `Optional` 类型，默认 `None`

## 示例
```python
class User(SQLModel, table=True):
    """用户表 - 后台系统用户管理"""
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True, description="用户ID")
    username: str = Field(unique=True, index=True, description="用户名")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")
```
