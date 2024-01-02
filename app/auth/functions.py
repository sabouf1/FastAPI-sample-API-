from passlib.context import CryptContext
from ..database import SessionLocal
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Optional
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .config import *
from .. import models

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
  
        
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)