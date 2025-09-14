from fastapi import HTTPException, status


unauth_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
)

token_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token error"
)

user_not_found_error = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)

user_inact_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive"
)

admin_error =  HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
)
