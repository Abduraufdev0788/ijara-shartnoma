from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.courses import Course
from ..schemas.courses import CourseCreate, CourseUpdate, CourseResponse

router = APIRouter(prefix="/courses", tags=["courses"])

# GET all courses
@router.get("/", response_model=List[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

# GET single course
@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# POST create course
@router.post("/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.name == course.name).first()
    if db_course:
        raise HTTPException(status_code=400, detail="Course already exists")

    new_course = Course(name=course.name)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# PUT update course
@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course_update: CourseUpdate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if course_update.name:
        # Yangi nom takrorlanmasligini tekshirish
        existing_course = db.query(Course).filter(Course.name == course_update.name, Course.id != course_id).first()
        if existing_course:
            raise HTTPException(status_code=400, detail="Course name already exists")
        course.name = course_update.name

    db.commit()
    db.refresh(course)
    return course

# DELETE course
@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}

# GET course groups
@router.get("/{course_id}/groups")
def get_course_groups(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return course.groups