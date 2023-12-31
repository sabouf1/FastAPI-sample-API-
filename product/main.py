from typing import List
from fastapi import FastAPI, Depends
from . import models 
from .database import SessionLocal, engine
from .routers import product,seller, seller_login,user
import logging



app = FastAPI(
  title = "My Products API",
  description = "Get the details for all products on our website",
  terms_of_service='https://github.com/sabouf1/FastAPI-sample-API-',
  
  contact={
    'Developer Name' : 'Said B.',
    'website' : 'https://github.com/sabouf1/FastAPI-sample-API-',
    'Email' : "said.boufares.@aol.com"
  }
)

app.include_router(product.router)
app.include_router(seller.router)
app.include_router(seller_login.router)
app.include_router(user.router)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}