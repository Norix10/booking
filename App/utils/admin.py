from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from App.models.users import User
from App.utils.user_utils import get_current_auth_user, get_user_by_sub
from App.utils.jwt_utils import decode_jwt
from App.utils.exc import admin_error
from App.db.db_helper import db_helper

bearer_scheme = HTTPBearer()


async def admin_required(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session=Depends(db_helper.get_db),
):
    token = credentials.credentials
    payload = decode_jwt(token)
    user = await get_user_by_sub(payload, session)
    if not user.is_admin:
        raise admin_error
    return user
