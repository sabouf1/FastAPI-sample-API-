from pydantic import BaseModel
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
  token_type: str
  