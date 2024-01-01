from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
from sqlalchemy.orm import joinedload
from ..auth.functions import get_db



router = APIRouter(
  prefix='/cart',
  tags=['Cart']
)
 

@router.get("/{user_id}", response_model=List[schemas.ShoppingCartItemDisplay])
def get_cart_items(user_id: int, db: Session = Depends(get_db)):
    items = db.query(models.ShoppingCartItem)\
              .filter(models.ShoppingCartItem.user_id == user_id)\
              .options(joinedload(models.ShoppingCartItem.product))\
              .all()
    return items


@router.post("/", response_model=schemas.ShoppingCartItemDisplay)
def add_item_to_cart(item: schemas.ShoppingCartItemBase, db: Session = Depends(get_db)):
    new_item = models.ShoppingCartItem(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put("/{item_id}", response_model=schemas.ShoppingCartItemDisplay)
def update_cart_item(item_id: int, item_update: schemas.ShoppingCartItemBase, db: Session = Depends(get_db)):
    item = db.query(models.ShoppingCartItem).filter(models.ShoppingCartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item_update.dict().items():
        setattr(item, key, value)
    db.commit()
    return item


@router.delete("/{item_id}", status_code=204)
def delete_cart_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.ShoppingCartItem).filter(models.ShoppingCartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"detail": "Item removed from cart"}
