from fastapi import APIRouter, Depends, HTTPException, status

# from  schemas import database,models,token
from utils.hashing import Hash
from utils import token
from models.User import User
from schemas.User import UserOut, UserIn, UserLogin
from sqlmodel import select

from config.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserOut)
async def create_user(request: UserIn, session: AsyncSession = Depends(get_session)):
    new_user = User(
        id=str(uuid.uuid4()),
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    await session.close()
    return new_user


@router.post("/login")
async def login(request: UserLogin, session: AsyncSession = Depends(get_session)):
    try:
        res = await session.execute(select(User).where(request.email == User.email))
        user = res.scalar_one()
        await session.close()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )

    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect UserName or Password",
        )

    # generate a jwt token
    access_token = token.create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
