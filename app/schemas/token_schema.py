from typing import Optional

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    algorithm: str = "HS256"
    time_expire: int = 15


class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
    # secret_key: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
