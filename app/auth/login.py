from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..schemas import *
from .. import models, schemas, database
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from ..database import SessionLocal, engine
from .functions import get_db
from typing import List
import logging
from .functions import *
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
  prefix='/login',
  tags=['Login']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.info("Decoding JWT token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.warning("Username not found in token payload")
            raise credentials_exception

        logger.info(f"Retrieved username {username} from token")        
        token_data = schemas.TokenData(username=username)  
    except JWTError as e :
        logger.error(f"Error decoding JWT token: {e}")    
        raise credentials_exception

    # user = db.query(models.User).filter(models.User.username == username).first()
    # if user is None:
    #     raise credentials_exception
    # return user

@router.post('/')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")  
    if not verify_password(request.password, user.hashed_password):
        print(verify_password(request.password, user.hashed_password))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")
    # Generate a JWT token
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires )
    return {"access_token": access_token, "token_type": "bearer"}