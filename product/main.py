from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
import logging



app = FastAPI(
  title = "My Products API",
  description = "Get the details for all products on our website",
  terms_of_service='https://github.com/sabouf1/FastAPI-sample-API-',
  
  contact={
    'Developer Name' : 'Said B.',
    'website' : 'https://github.com/sabouf1/FastAPI-sample-API-',
    'Email' : "said.boufares.@aol.com"
  }
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.post('/product', response_model=schemas.Product, tags=['Products'])
def add_product(product: schemas.Product):
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
  
  
@app.get(
  '/product/{product_id}', response_model=schemas.Product, tags=['Products'])
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.get('/products', response_model=List[schemas.Product], tags=['Products'])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()
 
@app.post('/seller', response_model=schemas.SellerDisplay, tags=['Sellers'])
def add_seller(seller: schemas.SellerCreate):
    db = SessionLocal()
    db_seller = models.Seller(username=seller.username, email=seller.email, password=seller.password)
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    db.close()
    return db_seller

@app.get('/seller/{seller_id}', response_model=schemas.Seller, tags=['Sellers'])
def get_seller(seller_id: int, db: Session = Depends(get_db)):
    seller_id = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if seller_id is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller_id
  
  
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}