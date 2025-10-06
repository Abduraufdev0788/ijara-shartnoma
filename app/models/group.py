from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))

    course = relationship("Course", back_populates="groups")
    students = relationship("Student", back_populates="group", lazy="dynamic")