from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import *
from .. import models, schemas, database
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from ..database import SessionLocal, engine
from ..auth.functions import get_db
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter

ph = PasswordHasher()

router = APIRouter(
  prefix='/users',
  tags=['Users']
)

 


@router.get('/', response_model=List[schemas.UserDisplay])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post('/', response_model=schemas.UserDisplay, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, email=user.email, hashed_password=user.password)  # Here, hash the password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get('/{user_id}', response_model=schemas.UserDisplay)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put('/{user_id}', response_model=schemas.UserDisplay)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db_user.hashed_password = user.password  # Again, hash the password here
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}