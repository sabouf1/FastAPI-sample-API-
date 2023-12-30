from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.post('/product', response_model=schemas.Product)
def add_product(product: schemas.ProductCreate):
    db = SessionLocal()
    db_product = models.Product(name=product.name, description=product.description, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db.close()
    return db_product
  
  
@app.get('/product/{product_id}', response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.get('/products', response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()
 
@app.post('/seller', response_model=schemas.Seller)
def add_seller(seller: schemas.SellerCreate):
    db = SessionLocal()
    db_seller = models.Seller(username=seller.username, email=seller.email, password=seller.password)
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    db.close()
    return db_seller

@app.get('/seller/{seller_id}', response_model=schemas.Seller)
def get_seller(seller_id: int, db: Session = Depends(get_db)):
    seller_id = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if seller_id is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller_id