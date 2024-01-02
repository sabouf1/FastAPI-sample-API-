from typing import List
from fastapi import FastAPI, Depends
from .auth import seller, user, login
from . import models 
from .database import SessionLocal, engine
from .routers import order, product, reviews, cart, wishlist
import logging



app = FastAPI(
  title = "My Products API - Powered by FastAPI",
  description = "Said B.",
  version = "1.0.0",
  terms_of_service = "https://github.com/sabouf1/FastAPI-sample-API-/blob/main/TERMS.md",
  contact = {
    "Developer Name": "Said B.",
    "Website": "https://github.com/sabouf1/FastAPI-sample-API-",
    "Email": "said.boufares.@aol.com"
  },
  license_info = {
    "name": "MIT License",
    "url": "https://github.com/sabouf1/FastAPI-sample-API-/blob/main/LICENSE"
  }
)


app.include_router(user.router)
app.include_router(seller.router)
app.include_router(order.router)
app.include_router(product.router)
app.include_router(reviews.router)
app.include_router(cart.router)
app.include_router(wishlist.router)
app.include_router(login.router)


models.Base.metadata.create_all(bind=engine)


        
        
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}