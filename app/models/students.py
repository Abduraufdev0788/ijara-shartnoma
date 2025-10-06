from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)

    students_number = Column(
        String, unique=True, nullable=False,
        comment="Unique student number"
    )
    price = Column(Integer, nullable=False, comment="Student dormitory fee")
    home_full_name = Column(String, nullable=False)
    home_number = Column(String, nullable=False, comment="Dormitory room number")
    location = Column(String, nullable=False, comment="Dormitory location")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="Record creation timestamp")
    
    group = relationship("Group", back_populates="students")
    