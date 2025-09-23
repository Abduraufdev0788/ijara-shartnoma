from sqlalchemy import Column, Integer, String, ForeignKey
from ..database import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, comment="Group identifier, e.g. MT23_10")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    