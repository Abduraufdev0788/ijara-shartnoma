from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.students import Student
from ..schemas.students import StudentCreate
from ..schemas.students import StudentUpdate


router = APIRouter(
    prefix="/students",
    tags=["students"]
)


@router.get("/")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students


@router.get("/group/{group_id}")
def get_students_by_group(group_id: int, db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.group_id == group_id).all()
    return students


@router.post("/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        full_name=student.full_name,
        course_id=student.course_id,
        group_id=student.group_id,
        students_number=student.students_number,
        price=student.price,
        home_full_name=student.home_full_name,
        home_number=student.home_number,
        location=student.location,
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.put("/{student_id}")
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")


    update_data = student.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student