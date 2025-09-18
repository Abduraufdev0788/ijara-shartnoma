from pydantic import BaseModel

class GroupCreate(BaseModel):
    name: str
    course_id: int   # qaysi kursga tegishli
