from passlib.context import CryptContext
from ..database import SessionLocal

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


