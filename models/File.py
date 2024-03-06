from sqlmodel import Relationship, Field, SQLModel, ForeignKey, DateTime
from models.User import User
from datetime import datetime


class Files(SQLModel, table=True):
    file_id: str = Field(primary_key=True, index=True)
    filename: str
    url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    size: int
    result: str
    user_id: str = Field(ForeignKey("User.id"))
