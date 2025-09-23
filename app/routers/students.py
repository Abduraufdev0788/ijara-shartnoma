from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.students import Student
from ..schemas.students import StudentCreate, StudentUpdate, StudentOut
from typing import List

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=List[StudentOut])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()



@router.post("/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        full_name=student.full_name,
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



@router.put("/{student_id}", response_model=StudentOut)
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student topilmadi")

    for key, value in student.model_dump(exclude_unset=True).items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student topilmadi")

    db.delete(db_student)
    db.commit()
    return {"detail": "Student o‘chirildi"}
