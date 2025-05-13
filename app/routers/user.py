from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..auth.auth import create_access_token, verify_password
from ..schemas import user as schemas_user
from ..crud import user as crud_user
from ..dependencies import get_db, get_current_user
from typing import List

router = APIRouter()

@router.get("/", response_model=List[schemas_user.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = crud_user.get_all_users(db=db)
    if not users:
        raise HTTPException(status_code=404, detail="No user was found")
    return users

@router.post("/register", response_model=schemas_user.UserResponse)
def register(user: schemas_user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db, user)

@router.post("/login", response_model=schemas_user.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db=db, email=form_data.username)
    
    if not user or verify_password(plain_password=form_data.password, hashed_password=user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile")
def read_profile(current_user: schemas_user.UserResponse = Depends(get_current_user)):
    return current_user