from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..import schemas,models
from ..schemas import TokenData
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
# from .seller import *
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..database import SessionLocal, engine

from jose import jwt, JWTError

SECRET_KEY = '2a9ec499cf629dd9a7ff48457f2cf5dc2b4742b90b05e9b6ff4d6130b6b74e8e'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

ph = PasswordHasher()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def generate_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({'exp': expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid password",
    headers={'WWW-Authenticate' : 'Bearer'}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get('sub')
    if username is None:
      raise credentials_exception
    
    token_data = TokenData(username=username)
  except JWTError:
    raise credentials_exception
 
  
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
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Incorrect Username or Password'
        )
        
    verify_password(request.password, seller.password)  
    
    access_token = generate_token(
      data={'sub': seller.username}
    )
    return {'access_token' : access_token, 'token_type' : 'bearer'}
    


