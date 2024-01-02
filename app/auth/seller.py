from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .functions import *
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, database, models
from .functions import get_db
from .login import create_access_token, get_current_user


router = APIRouter(
  prefix='/sellers',
  tags=['Sellers']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

    
    # Generate a JWT token
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/', response_model=List[schemas.SellerDisplay])
def get_sellers(db: Session = Depends(get_db), current_user: schemas.SellerDisplay = Depends(get_current_user)):
    sellers = db.query(models.Seller).all()
    return sellers

@router.post('/', response_model=schemas.SellerDisplay, status_code=status.HTTP_201_CREATED)
def create_seller(seller: schemas.SellerCreate, db: Session = Depends(get_db)):
    # Check for existing username or email in both User and Seller tables
    existing_user = db.query(models.User).filter((models.User.username == seller.username) | (models.User.email == seller.email)).first()
    existing_seller = db.query(models.Seller).filter((models.Seller.username == seller.username) | (models.Seller.email == seller.email)).first()

    if existing_user or existing_seller:
        raise HTTPException(status_code=400, detail="Username or email already in use")

    # Create new seller
    db_seller = models.Seller(username=seller.username, email=seller.email, hashed_password=hash_password(seller.password))
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
def update_seller(seller_id: int, seller: schemas.SellerCreate, db: Session = Depends(get_db), current_user: schemas.SellerDisplay = Depends(get_current_user)):
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
def delete_seller(seller_id: int, db: Session = Depends(get_db), current_user: schemas.SellerDisplay = Depends(get_current_user)):
    db_seller = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if db_seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    db.delete(db_seller)
    db.commit()
    return {"detail": "Seller deleted"}
