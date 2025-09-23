from pydantic import BaseModel

class CourseBase(BaseModel):
    name: str

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: str | None = None

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True
