from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from App.models.users import User
from App.schemas.users import UserCreate, UserLogin, UserRead
from App.utils.jwt_utils import hash_password, validate_password, decode_jwt
from App.db.db_helper import db_helper

bearer_scheme = HTTPBearer()


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


async def validate_auth_user(user_data: UserLogin, session: AsyncSession):
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
    )
    result = await session.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    if not user or not validate_password(user_data.password, user.hashed_password):
        raise unauth_exc
    return user


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(db_helper.get_db)
) -> User:
    token = credentials.credentials 
    payload = decode_jwt(token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token cannot be used here"
        )

    user_sub: str = payload.get("sub")
    if user_sub is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials",
        )

    result = await session.execute(select(User).where(User.email == user_sub))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserRead.model_validate(user)