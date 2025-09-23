from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StudentCreate(BaseModel):
    full_name: str
    students_number: str
    course_id: int
    group_id: int
    price: int
    home_full_name: str
    home_number: str
    location: str
    email: Optional[str] = None


class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    course_id: Optional[int] = None
    group_id: Optional[int] = None
    students_number: Optional[str] = None
    price: Optional[int] = None
    home_full_name: Optional[str] = None
    home_number: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None


class StudentResponse(BaseModel):
    id: int
    full_name: str
    course_id: int
    group_id: int
    students_number: str
    price: int
    home_full_name: str
    home_number: str
    location: str
    email: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True 