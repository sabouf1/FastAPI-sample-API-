from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, database, models

router = APIRouter()

router = APIRouter(
  tags=['Order Details']
)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/orders/{order_id}/details', response_model=schemas.OrderDetailDisplay, status_code=status.HTTP_201_CREATED)
def add_order_detail(order_id: int, order_detail: schemas.OrderDetailBase, db: Session = Depends(get_db)):
    # Check if the order exists
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db_order_detail = models.OrderDetail(**order_detail.dict(), order_id=order_id)
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

@router.get('/orders/{order_id}/details', response_model=List[schemas.OrderDetailDisplay])
def get_order_details(order_id: int, db: Session = Depends(get_db)):
    order_details = db.query(models.OrderDetail).filter(models.OrderDetail.order_id == order_id).all()
    return order_details

@router.put('/orders/details/{detail_id}', response_model=schemas.OrderDetailDisplay)
def update_order_detail(detail_id: int, order_detail_update: schemas.OrderDetailBase, db: Session = Depends(get_db)):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == detail_id).first()
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="Order detail not found")

    for key, value in order_detail_update.dict().items():
        setattr(db_order_detail, key, value)

    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

@router.delete('/orders/details/{detail_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order_detail(detail_id: int, db: Session = Depends(get_db)):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == detail_id).first()
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="Order detail not found")

    db.delete(db_order_detail)
    db.commit()
    return {"detail": "Order detail deleted"}
