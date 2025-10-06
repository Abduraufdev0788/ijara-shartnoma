from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from ..database import get_db
from ..models.students import Student
from ..models.group import Group
from ..schemas.students import StudentCreate, StudentUpdate, StudentResponse, StudentWithGroupResponse

router = APIRouter(prefix="/students", tags=["students"])

# GET all students with group info
@router.get("/", response_model=List[StudentWithGroupResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).options(joinedload(Student.group)).all()
    return students

# GET single student with group info
@router.get("/{student_id}", response_model=StudentWithGroupResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).options(joinedload(Student.group)).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# POST create student
@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Student raqami takrorlanmasligini tekshirish
    db_student = db.query(Student).filter(Student.students_number == student.students_number).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Student number already exists")

    # Group mavjudligini tekshirish
    group = db.query(Group).filter(Group.id == student.group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    new_student = Student(
        full_name=student.full_name,
        group_id=student.group_id,
        students_number=student.students_number,
        price=student.price,
        home_full_name=student.home_full_name,
        home_number=student.home_number,
        location=student.location
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# PUT update student
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student_update.students_number:
        existing_student = db.query(Student).filter(
            Student.students_number == student_update.students_number, 
            Student.id != student_id
        ).first()
        if existing_student:
            raise HTTPException(status_code=400, detail="Student number already exists")
        student.students_number = student_update.students_number

    if student_update.group_id:
        # Yangi group mavjudligini tekshirish
        group = db.query(Group).filter(Group.id == student_update.group_id).first()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        student.group_id = student_update.group_id

    if student_update.full_name:
        student.full_name = student_update.full_name
    if student_update.price is not None:
        student.price = student_update.price
    if student_update.home_full_name:
        student.home_full_name = student_update.home_full_name
    if student_update.home_number:
        student.home_number = student_update.home_number
    if student_update.location:
        student.location = student_update.location

    db.commit()
    db.refresh(student)
    return student

# DELETE student
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}