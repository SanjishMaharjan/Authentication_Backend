from fastapi import status, HTTPException, Depends


# from users import schemas, models
from schemas.User import UserIn
from models.User import User
from utils.hashing import Hash
import uuid
from config.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession


async def create_user(request: UserIn, session: AsyncSession = Depends(get_session)):
    new_user = User(
        id=str(uuid.uuid4()),
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )

    await session.add(new_user)
    await session.commit()
    session.refresh(new_user)
    return new_user
