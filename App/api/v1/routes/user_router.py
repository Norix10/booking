from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from db.db_helper import db_helper
from utils.tokens_helper import TokenInfo
from schemas.users import UserLogin, UserRead, UserCreate
from utils.user_utils import create_user, validate_auth_user
from utils.tokens_helper import create_access_token, create_refresh_token

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    async with db_helper.session_factory() as session:
        user = await create_user(user_data, session)
    return user


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(user_data: UserLogin, session: AsyncSession = Depends(db_helper.get_scoped_session)):
    user = await validate_auth_user(user_data, session)
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo.model_validate({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    })
