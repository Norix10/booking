from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from App.db.db_helper import db_helper
from App.schemas.users import UserRead
from App.models.users import User
from App.utils.admin import admin_required
from App.utils.exc import user_inact_error

router = APIRouter(tags=["admin"])


@router.patch("/users/{user_id}/toggle-active/", response_model=UserRead)
async def toggle_user_active(
    user_id: int,
    session: AsyncSession = Depends(db_helper.get_db),
    admin: User = Depends(admin_required),  # <- тут перевірка адміна через Bearer
):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise user_inact_error

    user.active = not user.active
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
