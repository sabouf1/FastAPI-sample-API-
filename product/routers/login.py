from fastapi import APIRouter, Depends, status, HTTPException
from ..import schemas,database,models
from argon2.exceptions import VerifyMismatchError
from .seller import *
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = '2a9ec499cf629dd9a7ff48457f2cf5dc2b4742b90b05e9b6ff4d6130b6b74e8e'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20

router = APIRouter()

ph = PasswordHasher()

def generate_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({'exp': expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorith=ALGORITHM)
  return encoded_jwt


# Function to verify the password
def verify_password(plain_password, hashed_password):
    try:
        ph.verify(hashed_password, plain_password)
        return ph.check_needs_rehash(hashed_password)
    except VerifyMismatchError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )
      
@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Incorrect Username or Password'
        )

    # Use the verify_password function
    verify_password(request.password, seller.password)
    
    # Login successful, return a success message
    return {"message": "Login successful"}


