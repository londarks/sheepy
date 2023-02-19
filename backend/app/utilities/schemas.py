from typing import List, Union, Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    address: Optional[str] = None
    email: str
    phone: Optional[str] = None
    password: str

class Login(BaseModel):
    email: str
    password: str


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: Optional[int] = None
    image: Optional[str] = None


class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: str
    description: Optional[str] = None
    price: float
    quantity: Optional[int] = None
    image: Optional[str] = None