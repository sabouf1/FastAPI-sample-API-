from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from ..import models, schemas
from ..database import SessionLocal, engine
from typing import List
from argon2 import PasswordHasher
from .seller_login import *


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
def get_seller(seller_id: int, db: Session = Depends(get_db), current_user:schemas.Seller = Depends(get_current_user)):
    seller_id = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if seller_id is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller_id
  
@router.put('/{seller_id}', response_model=schemas.SellerDisplay)
async def update_user(seller_id: int, 
                      user_update: schemas.SellerUpdate, db: Session = Depends(get_db) , 
                      current_user: schemas.SellerDisplay = Depends(get_current_user)):
    db = SessionLocal()
    seller = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    
    if not seller:
      raise HTTPException(status_code=404, detail="User not found")

    for var, value in vars(user_update).items():
        if value is not None:
            setattr(seller, var, value)    

    db.add(seller)
    db.commit()
    db.refresh(seller)
    db.close()
    return seller
  
@router.delete('/sellers/{seller_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_seller(seller_id: int, db: Session = Depends(get_db), current_user: schemas.SellerDisplay = Depends(get_current_user)):
    # Retrieve the seller to be deleted
    seller = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    # Delete the seller
    db.delete(seller)
    db.commit()

    return {"detail": "Seller successfully deleted"}