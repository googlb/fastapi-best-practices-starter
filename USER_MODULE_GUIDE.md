# 用户模块使用指南

## 概述

用户模块实现了系统认证功能，包括用户注册、登录和基于 JWT 的身份验证。

## 快速开始

### 1. 数据库迁移

首先生成并应用数据库迁移：

```bash
# 生成迁移文件
alembic revision --autogenerate -m "Add user table"

# 应用迁移
alembic upgrade head
```

### 2. 初始化 Admin 用户

```bash
python scripts/init_admin.py
```

输出示例：
```
✓ Admin user created successfully
  Username: admin
  Email: admin@example.com
  ID: 1
```

### 3. 登录获取 Token

使用 Swagger UI (`http://localhost:8000/docs`) 或 Scalar (`http://localhost:8000/scalar`)：

**POST** `/api/v1/users/login`

请求体：
```json
{
  "username": "admin",
  "password": "admin123"
}
```

响应：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 4. 使用 Token 访问受保护的端点

**GET** `/api/v1/users/me`

请求头：
```
Authorization: Bearer <access_token>
```

响应：
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "is_active": true,
  "is_superuser": true,
  "created_at": "2024-01-15T10:30:00"
}
```

## 项目结构

```
app/domains/user/
├── models.py      # User SQLModel 定义
├── schemas.py     # 请求/响应 DTO
├── crud.py        # 数据库操作
└── router.py      # 登录和用户信息端点

app/core/
└── security.py    # JWT 和密码哈希工具

app/dependencies/
├── auth.py        # 当前用户依赖注入
└── database.py    # 数据库会话依赖注入
```

## 核心功能

### 密码安全

- 使用 `bcrypt` 进行密码哈希
- 密码从不以明文存储

### JWT 认证

- **Access Token**: 短期令牌（默认 30 分钟），用于 API 请求
- **Refresh Token**: 长期令牌（默认 7 天），用于获取新的 access token

### 依赖注入

在路由中使用 `get_current_user` 依赖来保护端点：

```python
from app.dependencies.auth import get_current_user
from app.domains.user.models import User

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}
```

## 配置

在 `.env` 文件中配置 JWT 参数：

```env
SECRET_KEY=your_super_secret_key_change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## 遵循的架构规范

✓ **DDD 原则**: User 模块是独立的垂直切片  
✓ **防循环依赖**: User 模型在 `app/db/base.py` 中注册  
✓ **路由聚合**: 所有路由在 `app/api/v1/router.py` 中聚合  
✓ **异步优先**: 所有 IO 操作使用 `async/await`  
✓ **依赖注入**: 使用 FastAPI 的 `Depends` 进行依赖注入
