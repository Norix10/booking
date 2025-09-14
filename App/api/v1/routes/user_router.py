from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession


from App.db.db_helper import db_helper
from App.utils.tokens_helper import TokenInfo, AccessTokenOnly
from App.schemas.users import UserLogin, UserRead, UserCreate, UserUpdate
from App.utils.user_utils import (
    create_user,
    validate_auth_user,
    get_current_user_db,
    get_current_active_user,
    get_current_auth_user_for_refresh,
    update_user,
    delete_user,
)
from App.utils.tokens_helper import create_access_token, create_refresh_token
from App.models.users import User

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(tags=["users"], dependencies=[Depends(http_bearer)])


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


@router.post(
    "/refresh/", response_model=AccessTokenOnly, response_model_exclude_none=True
)
async def auth_refresh_jwt(user: UserRead = Depends(get_current_auth_user_for_refresh)):
    access_token = create_access_token(user)
    return AccessTokenOnly(access_token=access_token)


@router.get("/me/", response_model=UserRead)
async def auth_user_chek_self_info(user: UserRead = Depends(get_current_active_user)):
    return user


@router.patch("/me/", response_model=UserRead)
async def update_current_user(
    user_schema: UserUpdate,
    user: UserRead = Depends(get_current_user_db),
    session: AsyncSession = Depends(db_helper.get_db),
):
    updated_user = await update_user(user, user_schema, session)
    return updated_user


@router.delete("/me/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    user: UserRead = Depends(get_current_user_db),
    session: AsyncSession = Depends(db_helper.get_db),
):
    await delete_user(user, session)
    return {"message": "User deleted successfully!"}
