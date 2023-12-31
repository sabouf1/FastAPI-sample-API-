from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from .. import models, schemas
from .login import *
from ..database import SessionLocal, engine
from typing import List

router = APIRouter(
  tags=['Products'],
  prefix='/product'
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post('/', response_model=schemas.Product)
def add_product(product: schemas.Product, current_user:schemas.Seller = Depends(get_current_user)):
    db = SessionLocal()
    db_product = models.Product(
      name=product.name, 
      description=product.
      description, 
      price=product.price, 
      seller_id=1)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db.close()
    return db_product
  
  
@router.get('/{product_id}',response_model=schemas.Product)
def get_product(product_id: int, current_user:schemas.Seller = Depends(get_current_user), db: Session = Depends(get_db) ):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.get('/', response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db), current_user:schemas.Seller = Depends(get_current_user)):
    return db.query(models.Product).all()