from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Profile(BaseModel):
  name: str
  email: str
  age: int

class Product(BaseModel):
  name: str
  price: int
  discount: int
  discounted_price: float
    

@app.get('/')
def index():
  return 'Hello World'


@app.get('/products/{userid}/comments')
def profile(userid: int,commentid=None):
  return userid, commentid


@app.post('/adduser')
def adduser(profile: Profile):
  return profile.age

@app.post('/addproduct/{product_id}')
def addproduct(product: Product,product_id: int,category: str):
  product.discounted_price = product.price - (product.price * product.discount)/100
  product_data = product.model_dump()
  product_data['category'] = category
  return {
    'prd_id': product_id,
    'details': product_data
    }

