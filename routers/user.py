from fastapi import APIRouter, Depends, HTTPException
from schemas.User import UserIn, UserOut

# import controller.user as user_controller
from sqlmodel import select

from config.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from models.User import User

from utils.oauth2 import get_current_user


router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/profile", response_model=UserOut)
async def get_user(
    session: AsyncSession = Depends(get_session),
    user_id=Depends(get_current_user),
):
    print(f"{user_id=}")
    try:
        user = await session.get_one(User, user_id)
        return user

    except Exception:
        raise HTTPException(status_code=404, detail="User not found")
