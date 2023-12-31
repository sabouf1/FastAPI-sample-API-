from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from .. schemas import *
from .user import get_current_user, get_db
from typing import List

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


@router.get('/{order_id}')
async def get_order_by_order_id(order_id: int, db: Session = Depends(get_db), current_user: schemas.UserDisplay = Depends(get_current_user)  ):
  order = db.query(models.Order).filter(models.Order.id == order_id).first()
  if order is None:
    raise HTTPException(status_code=404, detail='Order Not Found')
  return order

@router.get('/', response_model=List[schemas.OrderDisplay])
async def get_current_user_orders(db: Session = Depends(get_db), 
                                  current_user: schemas.UserDisplay = Depends(get_current_user)):
    user_id = current_user.id  # Assuming the UserDisplay schema includes the user ID
    # Fetch orders for the current user
    orders = db.query(models.Order).filter(models.Order.user_id == user_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for the current user")
    return orders
  
  
@router.get('/orders/', response_model=List[schemas.OrderDisplayExtended])
async def get_orders(db: Session = Depends(get_db),
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None,
                     status: Optional[str] = None,
                     user_id: Optional[int] = None,
                     product_id: Optional[int] = None,
                     skip: int = 0, limit: int = 10):
    query = db.query(models.Order)

    if start_date and end_date:
        query = query.filter(models.Order.created_at >= start_date,
                             models.Order.created_at <= end_date)

    if status:
        query = query.filter(models.Order.order_status == status)

    if user_id:
        query = query.filter(models.Order.user_id == user_id)

    if product_id:
        query = query.filter(models.Order.product_id == product_id)

    # Implementing pagination
    orders = query.offset(skip).limit(limit).all()

    return orders