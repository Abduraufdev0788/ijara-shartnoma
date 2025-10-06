from sqlalchemy import Column, Integer, String
from ..database import Base
from sqlalchemy.orm import relationship, Session
from .group import Group

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    groups = relationship("Group", back_populates="course")



def get_course_with_groups(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()

def get_course_groups(db: Session, course_id: int):
    return db.query(Group).filter(Group.course_id == course_id).all()