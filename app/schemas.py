from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime
from typing import List, Optional

###########

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserDisplay(UserBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True
        
###########

# Seller Schemas
class SellerBase(BaseModel):
    username: str
    email: str

class SellerCreate(SellerBase):
    password: str

class SellerDisplay(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        orm_mode = True

###########

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    seller_id: int

class ProductDisplay(ProductBase):
    id: int
    seller: SellerDisplay
    class Config:
        orm_mode = True
        
###########

# OrderDetail Schemas
class OrderDetailBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int

class OrderDetailCreate(BaseModel):
    product_id: int
    quantity: int
    
class OrderDetailUpdate(BaseModel):
    id: int
    quantity: Optional[int]
    product_id: int
    
class OrderDetailDisplay(OrderDetailBase):
    id: int
    product_id: Optional[int]
    class Config:
        orm_mode = True

###########

# Order Schemas
class OrderBase(BaseModel):
    user_id: int

class OrderCreate(BaseModel):
    user_id: int
    order_details: List[OrderDetailCreate]
    seller_id: int
    
class OrderUpdate(BaseModel):
    status: str 
    order_details: Optional[List[OrderDetailUpdate]]

class OrderDisplay(OrderBase):
    id: int
    created_at: datetime  
    seller: SellerDisplay
    order_details: List[OrderDetailDisplay]
    class Config:
        orm_mode = True
 
###########

# Review Schemas
class ReviewBase(BaseModel):
    content: str
    user_id: int
    product_id: int
    order_id: int  # New field
    seller_id: int  # New field

class ReviewDisplay(ReviewBase):
    id: int
    class Config:
        orm_mode = True
        
###########

# ShoppingCartItem Schemas
class ShoppingCartItemBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class ShoppingCartItemDisplay(BaseModel):
    id: int
    user_id: int
    quantity: int
    product: Optional[ProductDisplay]  # Make sure this matches the name in the SQLAlchemy model
    class Config:
        orm_mode = True
        
###########

# WishlistItem Schemas
class WishlistItemBase(BaseModel):
    user_id: int
    product_id: int

class WishlistItemDisplay(WishlistItemBase):
    id: int
    class Config:
        orm_mode = True
        
###########        

class TokenData(BaseModel):
  pass