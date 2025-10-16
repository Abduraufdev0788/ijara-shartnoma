from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.group import Group
from ..schemas.groups import GroupCreate, GroupUpdate, GroupResponse

router = APIRouter(prefix="/groups", tags=["groups"])

# GET all or filter by id
@router.get("/", response_model=List[GroupResponse])
def get_groups(id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    if id:
        group = db.query(Group).filter(Group.id == id).all()
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        return group
    return db.query(Group).all()

# GET single group
@router.get("/{group_id}", response_model=GroupResponse)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

# POST create group
@router.post("/", response_model=GroupResponse)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    db_group = db.query(Group).filter(Group.name == group.name).first()
    if db_group:
        raise HTTPException(status_code=400, detail="Group already exists")

    new_group = Group(name=group.name, course_id=group.course_id)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

# PUT update group
@router.put("/{group_id}", response_model=GroupResponse)
def update_group(group_id: int, group_update: GroupUpdate, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if group_update.name:
        existing = db.query(Group).filter(Group.name == group_update.name, Group.id != group_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Group name already exists")
        group.name = group_update.name

    if group_update.course_id:
        group.course_id = group_update.course_id

    db.commit()
    db.refresh(group)
    return group

# DELETE group
@router.delete("/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    db.delete(group)
    db.commit()
    return {"message": "Group deleted successfully"}
