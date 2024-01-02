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
        account_type: str = payload.get("type")
        if username is None or account_type is None:
            logger.warning("Username or account type not found in token payload")
            raise credentials_exception

        logger.info(f"Retrieved username {username} and account type {account_type} from token")
        
        if account_type == "user":
            account = db.query(models.User).filter(models.User.username == username).first()
        elif account_type == "seller":
            account = db.query(models.Seller).filter(models.Seller.username == username).first()
        else:
            raise credentials_exception

        if account is None:
            raise credentials_exception

        return account

    except JWTError as e:
        logger.error(f"Error decoding JWT token: {e}")
        raise credentials_exception


@router.post('/')
def login(request: schemas.Login  , db: Session = Depends(get_db)):
    # Check both User and Seller tables
    user = db.query(models.User).filter(models.User.username == request.username).first()
    seller = db.query(models.Seller).filter(models.Seller.username == request.username).first()

    # Determine the account type
    account = user if user else seller
    account_type = "user" if user else "seller"
    
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not verify_password(request.password, account.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")

    # Generate JWT token with account type
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": account.username, "type": account_type},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
  
