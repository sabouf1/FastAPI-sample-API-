from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from .database import Base
from sqlalchemy.orm import relationship

class Product(Base):
  __tablename__ = 'products'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  description = Column(String)
  price = Column(Integer)
  seller_id = Column(Integer, ForeignKey('sellers.id'))
  
  seller = relationship("Seller", back_populates="product")
  reviews = relationship("Review", back_populates="product")
  order_details = relationship("OrderDetail", back_populates="product")


class Seller(Base):
  __tablename__= 'sellers'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String)
  email = Column(String)
  hashed_password  = Column(String)
  
  product = relationship("Product" , back_populates='seller') 
  orders = relationship("Order" , back_populates='seller') 
  
class User(Base):
  __tablename__= 'users'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  hashed_password  = Column(String)
  is_active = Column(Boolean, default=True)
  is_admin = Column(Boolean, default=False)
  
  orders = relationship("Order", back_populates="user")
  reviews = relationship("Review", back_populates="user")

class Order(Base):
  __tablename__ = 'orders'
  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey('users.id'))
  seller_id = Column(Integer, ForeignKey('sellers.id'))
  status = Column(String, default="Pending")
  created_at = Column(DateTime(timezone=True), server_default=func.now())

  # Relationships
  user = relationship("User", back_populates="orders")
  seller = relationship("Seller", back_populates="orders")
  order_details = relationship("OrderDetail", back_populates="orders")  
  
class OrderDetail(Base):
  __tablename__ = "order_details"
  id = Column(Integer, primary_key=True, index=True)
  order_id = Column(Integer, ForeignKey("orders.id"))
  seller_id = Column(Integer, ForeignKey('sellers.id'))
  
  product_id = Column(Integer, ForeignKey("products.id"))
  quantity = Column(Integer)
  
  
  orders = relationship("Order", back_populates="order_details")
  product = relationship("Product", back_populates="order_details")
  

class Review(Base):
  __tablename__ = "reviews"
  id = Column(Integer, primary_key=True, index=True)
  content = Column(String)
  user_id = Column(Integer, ForeignKey("users.id"))
  product_id = Column(Integer, ForeignKey("products.id"))

  user = relationship("User", back_populates="reviews")
  product = relationship("Product", back_populates="reviews")
    

class ShoppingCartItem(Base):
    __tablename__ = "shopping_cart_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)

class WishlistItem(Base):
    __tablename__ = "wishlist_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))