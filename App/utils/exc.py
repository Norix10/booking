from fastapi import HTTPException, status


unauth_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
)

token_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token error"
)

user_inact_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="User is not active"
)