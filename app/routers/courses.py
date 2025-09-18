from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.course import Course
from ..schemas.courses import CourseCreate

router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)

# Kurslar ro'yxati
@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses


@router.post("/")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(name=course.name)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course