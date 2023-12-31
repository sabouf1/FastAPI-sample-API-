from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from .database import Base
from sqlalchemy.orm import relationship

class Product(Base):
  __tablename__ = 'products'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  description = Column(String)
  price = Column(Integer)
  seller_id = Column(Integer, ForeignKey('sellers.id'))
  seller = relationship("Seller" , back_populates='products', lazy='joined') 

class Seller(Base):
  __tablename__= 'sellers'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String)
  email = Column(String)
  password = Column(String)
  products = relationship("Product" , back_populates='seller') 
  
class User(Base):
  __tablename__= 'users'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  password = Column(String)
  is_active = Column(Boolean, default=True)
  is_admin = Column(Boolean, default=False)