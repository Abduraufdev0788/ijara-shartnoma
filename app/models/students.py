from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from datetime import datetime
from ..database import Base
from typing import Optional
from pydantic import BaseModel

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    students_number = Column(String, unique=True, index=True, comment="Unique student number", nullable=False)
    price = Column(Integer, comment="Student dormitory fee", nullable=False)
    home_full_name = Column(String, index=True, nullable=False)
    home_number = Column(String, comment="Dormitory room number", nullable=False)
    location = Column(String, comment="Dormitory location", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="Record creation timestamp") 

   
class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    course_id: Optional[int] = None
    group_id: Optional[int] = None
    students_number: Optional[str] = None
    price: Optional[int] = None
    home_full_name: Optional[str] = None
    home_number: Optional[str] = None
    location: Optional[str] = None
