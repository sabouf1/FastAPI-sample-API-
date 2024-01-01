from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(
  prefix='/reviews',
  tags=['Reviews']
)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ReviewDisplay, status_code=201)
def create_review(review: schemas.ReviewBase, db: Session = Depends(get_db)):
    new_review = models.Review(**review.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/", response_model=List[schemas.ReviewDisplay])
def read_reviews(db: Session = Depends(get_db)):
    reviews = db.query(models.Review).all()
    return reviews

@router.get("/{review_id}", response_model=schemas.ReviewDisplay)
def read_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=schemas.ReviewDisplay)
def update_review(review_id: int, review_update: schemas.ReviewBase, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    for key, value in review_update.dict().items():
        setattr(review, key, value)
    db.commit()
    return review

@router.delete("/{review_id}", status_code=204)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"detail": "Review deleted"}
