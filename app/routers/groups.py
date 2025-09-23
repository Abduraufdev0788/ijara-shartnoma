from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.group import Group
from ..schemas.groups import GroupCreate, GroupUpdate, GroupOut

router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)

@router.get("/", response_model=list[GroupOut])
def get_groups(db: Session = Depends(get_db)):
    return db.query(Group).all()

@router.post("/")
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    new_group = Group(name=group.name, course_id=group.course_id)  # ✅ dict emas
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


@router.put("/{group_id}", response_model=GroupOut)
def update_group(group_id: int, update: GroupUpdate, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    for var, value in update.dict(exclude_unset=True).items():
        setattr(group, var, value)

    db.commit()
    db.refresh(group)
    return group

@router.delete("/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(group)
    db.commit()
    return {"detail": "Group deleted successfully"}

