from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.courses import Course
from ..schemas.courses import CourseCreate, CourseResponse

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.post("/", response_model=CourseResponse)
def post_courses(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(name=course.name)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course