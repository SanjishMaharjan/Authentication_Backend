from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class FilesOut(BaseModel):
    file_id: str
    url: str
    size: int
    created_at: datetime
    result: str

    class Config:
        orm_mode = True


# To use response model we use this class to make it working


# class GetFiles(Files):
#     title: str
#     body: str

#     class Config:
#         from_attributes = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
