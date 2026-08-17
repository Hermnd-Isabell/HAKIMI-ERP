from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=3, max_length=120)
    password: str = Field(min_length=6, max_length=128)
    full_name: Optional[str] = Field(default=None, max_length=100)


class UserLogin(BaseModel):
    account: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=1, max_length=128)
    remember_me: bool = False


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_time: datetime
    last_login_time: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: UserOut
