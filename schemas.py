from pydantic import BaseModel

class Event(BaseModel):
    summary: str
    start: str
    end: str

    class Config:
        orm_mode = True
