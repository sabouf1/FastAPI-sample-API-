from pydantic import BaseModel,EmailStr
from typing import Optional


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
    
class SellerDisplay(BaseModel):
  username : str
  email : str
  
  class Config:
    orm_mode = True
    
class ProductBase(BaseModel):
  name: str
  description: str
  price: int
   
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
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
