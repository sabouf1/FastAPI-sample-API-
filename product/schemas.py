from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime




class SellerBase(BaseModel):
  username : str
  email : str
  password : str
  
class SellerCreate(SellerBase):
  pass

class Seller(SellerBase):
  id: int
  username : str
  email : str
  
  class Config:
    orm_mode = True
    
class UserUpdate(BaseModel):
  username: Optional[str] = None
  email: Optional[EmailStr] = None
  is_active: Optional[bool] = None
  is_admin: Optional[bool] = None
    
    
class SellerDisplay(BaseModel):
  username : str
  email : str
  
  class Config:
    orm_mode = True
    
class ProductBase(BaseModel):
  name: str
  description: str
  price: int

class SellerUpdate(BaseModel):
  username: Optional[str] = None
  email: Optional[EmailStr] = None
  is_active: Optional[bool] = None
  is_admin: Optional[bool] = None
       
class Product(ProductBase):
  id: int
  name : str
  description : str
  seller: SellerDisplay

  class Config:
    orm_mode = True    

class Login(BaseModel):
  username: str
  password: str
  
class Token(BaseModel):
  access_token: str
  token_type: str
  
class TokenData(BaseModel):
  username: Optional[str] = None
  
class UserBase(BaseModel):
  username: str
  email: EmailStr
  
class UserCreate(UserBase):
  password: str

class UserUpdate(UserBase):
  password: Optional[str] = None
  
class UserDisplay(UserBase):
  id: int
  is_active: bool
  is_admin: bool
    
  class Config:
    orm_mode = True
    
# Schema for creating a new order
class OrderCreate(BaseModel):
    product_id: int
    user_id: int
    quantity: int

class OrderDisplay(BaseModel):
    id: int
    product_id: int
    user_id: int
    quantity: int
    created_at: datetime

    class Config:
        orm_mode = True

class OrderDisplayExtended(OrderDisplay):
    product: Optional[Product]
    user: Optional[UserDisplay]

    
