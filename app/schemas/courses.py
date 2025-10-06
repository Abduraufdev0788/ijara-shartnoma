from pydantic import BaseModel
from typing import List
from .groups import GroupResponse

class CourseBase(BaseModel):
    name: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: str | None = None

class CourseResponse(CourseBase):
    id: int
    groups: List[GroupResponse] = []
    
    class Config:
        from_attributes = True