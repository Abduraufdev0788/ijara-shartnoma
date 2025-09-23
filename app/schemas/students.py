from pydantic import BaseModel
from datetime import datetime

class StudentBase(BaseModel):
    full_name: str
    group_id: int
    students_number: str
    price: int
    home_full_name: str
    home_number: str
    location: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    full_name: str | None = None
    group_id: int | None = None
    students_number: str | None = None
    price: int | None = None
    home_full_name: str | None = None
    home_number: str | None = None
    location: str | None = None

class StudentOut(StudentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
