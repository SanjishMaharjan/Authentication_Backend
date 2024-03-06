from pydantic import BaseModel
from typing import List, Optional


# To use response model we use this class to make it working


class UserIn(BaseModel):
    name: str
    email: str
    password: str


class UserOut(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str
