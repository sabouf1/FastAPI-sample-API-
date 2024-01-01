from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, database, models
import logging
from ..auth.functions import get_db



router = APIRouter()

logging.basicConfig(level=logging.INFO)


router = APIRouter(
  prefix='/orders',
  tags=['Orders']
)

 

@router.post('/', response_model=schemas.OrderDisplay, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.id == order.seller_id).first()
    if not seller:
      raise HTTPException(status_code=404, detail="Seller not found")
    
    db_order = models.Order(user_id=order.user_id, seller_id=seller.id)
    db.add(db_order)
    db.flush()  # Flush to get the order ID before committing

    for detail in order.order_details:
        db_detail = models.OrderDetail(order_id=db_order.id, **detail.model_dump())
        db.add(db_detail)

    db.commit()
    db.refresh(db_order)
    return db_order


@router.get('/{order_id}', response_model=schemas.OrderDisplay)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put('/{order_id}', response_model=schemas.OrderDisplay)
def update_order(order_id: int, order_update: schemas.OrderUpdate, db: Session = Depends(get_db)):
    # Fetch the existing order
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update the status
    db_order.status = order_update.status

    # Update order details if provided
    if order_update.order_details:
        existing_detail_ids = [detail.id for detail in db_order.order_details]
        for detail_update in order_update.order_details:
            # Check if the detail exists in the order
            if detail_update.id in existing_detail_ids:
                # Fetch and update the existing order detail
                db_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == detail_update.id).first()
                if detail_update.quantity is not None:
                    db_detail.quantity = detail_update.quantity
                # Update other fields as needed
            else:
                # Handle the case where the detail ID does not exist
                raise HTTPException(status_code=404, detail=f"Order detail with id {detail_update.id} not found in the order")

    # Commit the transaction
    db.commit()
    db.refresh(db_order)

    return db_order



@router.delete('/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # Delete the order; associated order details will be deleted automatically
    db.delete(order)
    db.commit()

    return {"detail": "Order and associated order details deleted"}

