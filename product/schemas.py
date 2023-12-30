from pydantic import BaseModel

class ProductBase(BaseModel):
  name: str
  description: str
  price: int

class ProductCreate(ProductBase):
  pass

class Product(ProductBase):
  id: int

  class Config:
    orm_mode = True
        

class SellerBase(BaseModel):
  username : str
  email : str
  password : str
  
class SellerCreate(SellerBase):
  pass

class Seller(SellerBase):
  id: int
  
  class Config:
    orm_mode = True