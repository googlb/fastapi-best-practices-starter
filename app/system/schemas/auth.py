from pydantic import BaseModel, Field, ConfigDict

# 1. 登录请求
class UserLogin(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

    # 文档默认示例
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "username": "admin",
                    "password": "abc123"
                }
            ]
        }
    )

# 2. Token 响应 (返回给前端的)
class TokenSchema(BaseModel):
    access_token: str = Field(serialization_alias="accessToken", description="访问令牌")
    refresh_token: str = Field(serialization_alias="refreshToken", description="刷新令牌")
    token_type: str = Field(default="Bearer", serialization_alias="tokenType", description="令牌类型")
    expires_in: int = Field(default=60 * 15, serialization_alias="expiresIn", description="过期时间(秒)")

# 3. 刷新 Token 请求
class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., serialization_alias="refreshToken", description="刷新令牌")

    # 文档默认示例
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                }
            ]
        }
    )
