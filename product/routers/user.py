from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import *
from .. import models, schemas, database
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from ..database import SessionLocal, engine
from .user_login import get_current_user
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
    db_user = models.User(username=user.username, email=user.email, password=hashed_password, is_admin=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

@router.get('/{user_name}', response_model=schemas.UserDisplay)
async def get_user_id(user_name: str, db: Session = Depends(get_db), current_user: schemas.UserDisplay = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.username == user_name).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
  
@router.get('/{user_id}', response_model=schemas.UserDisplay)
async def get_user_id(user_id: int, db: Session = Depends(get_db), current_user: schemas.UserDisplay = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
  
@router.get('/{user_id}', response_model=schemas.UserDisplay)
def get_user_id(user_id: int, db: Session = Depends(get_db), current_user: schemas.UserDisplay = Depends(get_current_user)):
    user  = db.query(models.User).filter(models.User.id == user_id).first()
    if user  is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user 
     
@router.get("/", response_model=List[schemas.UserDisplay])  
async def get_users(
    db: Session = Depends(get_db),
    current_user: schemas.UserDisplay = Depends(get_current_user),
    skip: int = 0,limit: int = 10,search: Optional[str] = None
    ):
    # Ensure the current user is authorized (e.g., an admin)
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")

    query = db.query(models.User)
    
    # Basic search functionality
    if search:
        query = query.filter(models.User.username.contains(search))

    users = query.offset(skip).limit(limit).all()
    return users
  
  
@router.put('/{user_id}', response_model=schemas.UserDisplay)
async def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db) , current_user: schemas.UserDisplay = Depends(get_current_user)):
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
      raise HTTPException(status_code=404, detail="User not found")

    for var, value in vars(user_update).items():
        if value is not None:
            setattr(user, var, value)    

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user