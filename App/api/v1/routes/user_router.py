from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from App.db.db_helper import db_helper
from App.utils.tokens_helper import TokenInfo
from App.schemas.users import UserLogin, UserRead, UserCreate
from App.utils.user_utils import create_user, validate_auth_user, get_current_user
from App.utils.tokens_helper import create_access_token, create_refresh_token
from App.models.users import User

router = APIRouter (tags=["users"])


@router.post("/register/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    async with db_helper.session_factory() as session:
        user = await create_user(user_data, session)
    return user


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user_data: UserLogin, session: AsyncSession = Depends(db_helper.get_db)
):
    user = await validate_auth_user(user_data, session)
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo.model_validate(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    )


@router.get("/me/", response_model=UserRead)
async def get_me(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.get_db),
):
    return current_user
