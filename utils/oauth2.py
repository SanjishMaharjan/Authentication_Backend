from fastapi import HTTPException, status, Header
from utils import token
from typing import Optional


def get_current_user(Bearer: Optional[str] = Header(None)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    user_id = token.verify_token(Bearer, credentials_exception)
    return user_id
