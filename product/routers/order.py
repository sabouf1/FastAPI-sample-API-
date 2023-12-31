from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from .. schemas import *
from .user import get_current_user, get_db

router = APIRouter(
  prefix='/order',
  tags=['Orders']
)

@router.post('/', response_model=schemas.OrderDisplay)
async def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: schemas.OrderDisplay = Depends(get_current_user)):
    # Check if the product exists
    product = db.query(models.Product).filter(models.Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if the user is valid
    user = db.query(models.User).filter(models.User.id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a new order
    new_order = models.Order(
        product_id=order.product_id,
        quantity=order.quantity,
        user_id=order.user_id
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order
