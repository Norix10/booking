from fastapi import HTTPException, status, Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from App.models.users import User
from App.schemas.users import UserCreate, UserLogin, UserRead, UserUpdate
from App.utils.jwt_utils import hash_password, validate_password, decode_jwt
from App.db.db_helper import db_helper
from App.utils.tokens_helper import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from App.utils.exc import unauth_error, token_error, user_inact_error

bearer_scheme = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


async def create_user(user_data: UserCreate, session: AsyncSession) -> User:
    hash_pwd = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_pwd,
        active=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def validate_auth_user(user_data: UserLogin, session: AsyncSession) -> User:
    result = await session.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    if not user or not validate_password(user_data.password, user.hashed_password):
        raise unauth_error
    return user


async def validate_token_type(payload: dict, token_type: str) -> bool:
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise token_error


async def get_current_token_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError:
        raise token_error
    return payload

async def get_current_user_db(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.get_db)
) -> User:
    email = payload.get("sub")
    if not email:
        raise token_error

    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise token_error
        
    return user


async def get_user_by_sub(
    payload: dict, session: AsyncSession = Depends(db_helper.get_db)
) -> UserRead:
    email = payload.get("sub")
    if not email:
        raise token_error

    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise token_error
    return UserRead.model_validate(user)


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
        self,
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(db_helper.get_db),
    ):
        await validate_token_type(payload, self.token_type)
        return await get_user_by_sub(payload, session)


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


async def get_current_active_user(
    user: UserRead = Depends(get_current_auth_user),
) -> UserRead:
    if user.active:
        return user
    raise user_inact_error


async def update_user(user: User, user_schema: UserUpdate, session: AsyncSession):
    if user_schema.password:
        user.hashed_password = hash_password(user_schema.password)

    for field, value in user_schema.model_dump(exclude_unset=True).items():
        if field != "password": 
            setattr(user, field, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def delete_user(user: User, session: AsyncSession) -> None:
    await session.delete(user)
    await session.commit()