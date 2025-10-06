from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
    full_name: Optional[str] = None
    group_id: Optional[int] = None
    students_number: Optional[str] = None
    price: Optional[int] = None
    home_full_name: Optional[str] = None
    home_number: Optional[str] = None
    location: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Group ma'lumotlari bilan student
class GroupInfo(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class StudentWithGroupResponse(StudentResponse):
    group: Optional[GroupInfo] = None
    
    class Config:
        from_attributes = True