from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.group import Group
from ..schemas.groups import GroupCreate, GroupUpdate, GroupResponse

router = APIRouter(prefix="/groups", tags=["groups"])

# ✅ GET all groups (optional course_id filter)
@router.get("/", response_model=List[GroupResponse])
def get_groups(course_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Group)
    if course_id:
        query = query.filter(Group.course_id == course_id)
    return query.all()

# ✅ GET single group
@router.get("/{group_id}", response_model=GroupResponse)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

# ✅ POST create group (course_id check added)
@router.post("/", response_model=GroupResponse)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    if not group.course_id:
        raise HTTPException(status_code=400, detail="Course ID is required")

    existing_group = db.query(Group).filter(Group.name == group.name, Group.course_id == group.course_id).first()
    if existing_group:
        raise HTTPException(status_code=400, detail="This group already exists in this course")

    new_group = Group(name=group.name, course_id=group.course_id)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

# ✅ PUT update
@router.put("/{group_id}", response_model=GroupResponse)
def update_group(group_id: int, group_update: GroupUpdate, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    if group_update.name:
        duplicate = db.query(Group).filter(
            Group.name == group_update.name,
            Group.course_id == group.course_id,
            Group.id != group_id
        ).first()
        if duplicate:
            raise HTTPException(status_code=400, detail="Group name already exists in this course")
        group.name = group_update.name

    if group_update.course_id:
        group.course_id = group_update.course_id

    db.commit()
    db.refresh(group)
    return group

# ✅ DELETE
@router.delete("/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    db.delete(group)
    db.commit()
    return {"message": "Group deleted successfully"}

# ✅ GET students by group
@router.get("/{group_id}/students")
def get_group_students(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group.students
