from typing import Optional
from datetime import datetime

import rfc3339
from pydantic import BaseModel, Field, ConfigDict


class Wallet(BaseModel):
    address: str = Field(pattern=r"^0x[a-fA-F0-9]{40}$")


class BotUser(BaseModel):
    full_name: str
    username: Optional[str]
    telegram_id: int
    is_premium: bool
    is_banned: bool
    language_code: Optional[str]
    joined_at: datetime
    last_active_at: datetime
    wallets: list[Optional[str]]

    model_config = ConfigDict(json_encoders={datetime: lambda v: rfc3339.rfc3339(v)})


class AdminUser(BaseModel):
    username: str = Field(min_length=4, max_length=32)
    hashed_password: str


class AdminAuth(BaseModel):
    username: str
    password: str = Field(min_length=5, max_length=32)


class BotUserUpdateData(BaseModel):
    full_name: str
    username: Optional[str]
    is_premium: bool
    language_code: Optional[str]
    last_active_at: datetime

    model_config = ConfigDict(json_encoders={datetime: lambda v: rfc3339.rfc3339(v)})


class LanguageStats(BaseModel):
    languages: dict[str, int]


class ActiveStats(BaseModel):
    active_users: dict[str, int]
    first_user_joined_at: Optional[datetime]
    last_user_active_at: Optional[datetime]

    model_config = ConfigDict(json_encoders={datetime: lambda v: rfc3339.rfc3339(v)})


class AllStats(BaseModel):
    total_users: int
    active_stats: ActiveStats
    banned_users: int
    premium_users: int
    language_stats: LanguageStats


class ResponseMsg(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
