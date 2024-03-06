from datetime import datetime
from typing import List


from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: str = Field(primary_key=True, index=True)
    name: str
    email: str
    password: str

    # files: List["Files"] = Relationship(back_populates="creator")
