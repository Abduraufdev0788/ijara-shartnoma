from sqlalchemy import Column, Integer, String
from ..database import Base
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

groups = relationship("Group", back_populates="course", cascade="all, delete-orphan")
