import asyncio
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .connection import Base

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)
    phone = Column(String)
    password = Column(String)

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', address='{self.address}', email='{self.email}', phone='{self.phone}', password='{self.password}')"


class Order(Base):
    __tablename__ = 'Order'
    id = Column(Integer, primary_key=True)
    date = Column(Float)
    total_amount = Column(Float)
    status = Column(String)
    user_id = Column(Integer)

    def __repr__(self):
        return f"Order(id={self.id}, date='{self.date}', total_amount={self.total_amount}, status='{self.status}', user_id={self.user_id})"


class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    image = Column(String)

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', description='{self.description}', price={self.price}, quantity={self.quantity}, image='{self.image}')"


class Ordem_item(Base):
    __tablename__ = 'Ordem_item'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    unit_price = Column(Float)
    discount = Column(Float)
    order_id = Column(Integer)
    product_id = Column(Integer)

    def __repr__(self):
        return f"Ordem_item(id={self.id}, quantity={self.quantity}, unit_price={self.unit_price}, discount={self.discount}, order_id={self.order_id}, product_id={self.product_id})"


class Cart(Base):
    __tablename__ = 'Cart'
    id = Column(Integer, primary_key=True)
    user = Column(Integer)

    def __repr__(self):
        return f"Cart(id={self.id}, user={self.user})"


class Payment(Base):
    __tablename__ = 'Payment'
    id = Column(Integer, primary_key=True)
    typee = Column(String)
    amount = Column(Float)
    order = Column(Integer)

    def __repr__(self):
        return f"Payment(id={self.id}, typee='{self.typee}', amount={self.amount}, order={self.order})"


class Inventory(Base):
    __tablename__ = 'Inventory'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    quantity = Column(Integer)
    last_updated = Column(Float)

    def __repr__(self):
        return f"Inventory(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, last_updated={self.last_updated})"