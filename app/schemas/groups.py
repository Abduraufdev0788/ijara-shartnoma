from pydantic import BaseModel

class GroupBase(BaseModel):
    name: str
    course_id: int

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: str | None = None
    course_id: int | None = None

class GroupOut(GroupBase):
    id: int

    class Config:
        orm_mode = True
