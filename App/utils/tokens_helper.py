from datetime import timedelta
from pydantic import BaseModel

from App.core.settings import settings
from App.utils.jwt_utils import decode_jwt, encode_jwt
from App.models.users import User

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class AccessTokenOnly(BaseModel):
    access_token: str

def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = token_data.copy()      
    jwt_payload["type"] = token_type
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user) -> str:
    jwt_payload = {
        "sub": user.email,
        "username": user.username,
        "email": user.email,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(user) -> str:
    jwt_payload = {
        "sub": user.email,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )
