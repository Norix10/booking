from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from models.users import User
from schemas.users import UserCreate, UserLogin, UserRead
from utils.jwt_utils import hash_password, validate_password


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
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
    )
    result = await session.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    if not user or not validate_password(user_data.password, user.hashed_password):
        raise unauth_exc
    return UserRead.model_validate(user)