from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import *
from .. import models, schemas, database
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from ..database import SessionLocal, engine
from .user_login import get_current_user

router = APIRouter

ph = PasswordHasher()

router = APIRouter(
  prefix='/users',
  tags=['Users']
)

# Dependency to get the DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/', response_model=schemas.UserDisplay)
def add_user(user: schemas.UserCreate):
    db = SessionLocal()
    hashed_password = ph.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


@router.get('/{user_id}', response_model=schemas.UserDisplay)
def get_user (user_id: int, db: Session = Depends(get_db)):
    user_id = db.query(models.User).filter(models.User.id == user_id).first()
    if user_id is None:
        raise HTTPException(status_code=404, detail="USER not found")
    return user_id