from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.dependencies import get_current_active_user, get_db

router = APIRouter()

@router.post("/", response_model=schemas.User,status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/me", response_model=schemas.User, tags=["users"])
def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=schemas.User, tags=["users"])
def update_user_me( user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    return crud.update_user(db=db, db_user=current_user, user=user)
