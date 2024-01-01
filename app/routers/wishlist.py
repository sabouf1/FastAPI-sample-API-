from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from .. database import SessionLocal
from ..auth.functions import get_db



router = APIRouter(
  prefix='/whishlist',
  tags=['Whishlist']
)
        
        
@router.post("/", response_model=schemas.WishlistItemDisplay, status_code=status.HTTP_201_CREATED)
def add_to_wishlist(wishlist_item: schemas.WishlistItemBase, db: Session = Depends(get_db)):
    new_item = models.WishlistItem(**wishlist_item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/user/{user_id}", response_model=List[schemas.WishlistItemDisplay])
def get_user_wishlist(user_id: int, db: Session = Depends(get_db)):
    items = db.query(models.WishlistItem).filter(models.WishlistItem.user_id == user_id).all()
    return items

@router.put("/{item_id}", response_model=schemas.WishlistItemDisplay)
def update_wishlist_item(item_id: int, item_update: schemas.WishlistItemBase, db: Session = Depends(get_db)):
    item = db.query(models.WishlistItem).filter(models.WishlistItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item.product_id = item_update.product_id
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_from_wishlist(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.WishlistItem).filter(models.WishlistItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"detail": "Item removed from wishlist"}
