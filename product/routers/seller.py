from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from ..import models, schemas
from ..database import SessionLocal, engine
from typing import List
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

router = APIRouter()

ph = PasswordHasher()

router = APIRouter(
  tags=['Sellers'],
  prefix='/seller'
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
@router.post('/', response_model=schemas.SellerDisplay)
def add_seller(seller: schemas.SellerCreate):
    db = SessionLocal()
    hashed_password = ph.hash(seller.password)
    db_seller = models.Seller(username=seller.username, email=seller.email, password=hashed_password)
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    db.close()
    return db_seller

@router.get('/{seller_id}', response_model=schemas.Seller)
def get_seller(seller_id: int, db: Session = Depends(get_db)):
    seller_id = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if seller_id is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller_id