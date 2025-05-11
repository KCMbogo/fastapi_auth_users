from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import user as schemas_user
from ..crud import user as crud_user
from ..dependencies import get_db
from typing import List

router = APIRouter()

@router.post("/register", response_model=schemas_user.UserResponse)
def register(user: schemas_user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db, user)

@router.get("/", response_model=List[schemas_user.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = crud_user.get_all_users(db=db)
    if not users:
        raise HTTPException(status_code=404, detail="No user was found")
    return users