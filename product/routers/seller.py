from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, database, models

router = APIRouter(
  prefix='/sellers',
  tags=['Sellers']
)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=List[schemas.SellerDisplay])
def get_sellers(db: Session = Depends(get_db)):
    sellers = db.query(models.Seller).all()
    return sellers

@router.post('/', response_model=schemas.SellerDisplay, status_code=status.HTTP_201_CREATED)
def create_seller(seller: schemas.SellerCreate, db: Session = Depends(get_db)):
    db_seller = models.Seller(username=seller.username, email=seller.email, hashed_password=seller.password)  # Hash the password
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller

@router.get('/{seller_id}', response_model=schemas.SellerDisplay)
def get_seller(seller_id: int, db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return seller

@router.put('/{seller_id}', response_model=schemas.SellerDisplay)
def update_seller(seller_id: int, seller: schemas.SellerCreate, db: Session = Depends(get_db)):
    db_seller = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if db_seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    db_seller.username = seller.username
    db_seller.email = seller.email
    db_seller.hashed_password = seller.password  # Hash the password here
    db.commit()
    db.refresh(db_seller)
    return db_seller

@router.delete('/{seller_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_seller(seller_id: int, db: Session = Depends(get_db)):
    db_seller = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if db_seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    db.delete(db_seller)
    db.commit()
    return {"detail": "Seller deleted"}
