from pydantic import BaseModel
from typing import List
from .students import StudentResponse

class GroupBase(BaseModel):
    name: str
    course_id: int

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: str | None = None
    course_id: int | None = None

class GroupResponse(GroupBase):
    id: int
    students: List[StudentResponse] = []
    
    class Config:
        from_attributes = True