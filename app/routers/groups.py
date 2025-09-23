from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.group import Group
from ..schemas.groups import GroupCreate

router = APIRouter(
    prefix="/groups",
    tags=["groups"]
)


@router.get("/")
def get_groups(db: Session = Depends(get_db)):
    groups = db.query(Group).all()
    return groups

@router.post("/")
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    new_group = Group(name=group.name, course_id=group.course_id)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group
