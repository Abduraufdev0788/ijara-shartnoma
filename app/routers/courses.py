from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.courses import Course

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()
