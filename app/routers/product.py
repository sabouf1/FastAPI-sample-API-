from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, database, models
from ..auth.functions import get_db



router = APIRouter(
  prefix='/products',
  tags=['Products']
)

  

@router.post('/products/', response_model=schemas.ProductDisplay, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # Here, you might want to check if the seller_id is valid
    seller = db.query(models.Seller).filter(models.Seller.id == product.seller_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get('/products/', response_model=List[schemas.ProductDisplay])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.get('/products/{product_id}', response_model=schemas.ProductDisplay)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put('/products/{product_id}', response_model=schemas.ProductDisplay)
def update_product(product_id: int, product_update: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product_update.dict().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete('/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted"}
