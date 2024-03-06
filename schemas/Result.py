from pydantic import BaseModel


class Result(BaseModel):
    result: str
    confidence: float
    type : str

    class Config:
        from_attributes = True