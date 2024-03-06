from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.File import Files
from models.User import User

from dotenv import load_dotenv
import os

load_dotenv()


username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
dbname = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")
db_host = os.getenv("DB_HOST")

DATABASE_URL = (
    f"postgresql+asyncpg://{username}:{password}@{db_host}:{db_port}/{dbname}"
)

engine = create_async_engine(DATABASE_URL, echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


engine = create_async_engine(DATABASE_URL, echo=True)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
