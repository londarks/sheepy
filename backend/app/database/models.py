import asyncio
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from .connection import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(EmailType)
    phone = Column(String)
    password = Column(String)

    tokens = relationship("Token", back_populates="user")
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, phone={self.phone})>"

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    access_token = Column(String)
    refresh_token = Column(String)

    user = relationship("User", back_populates="tokens")


    def __repr__(self):
        return f"Token(id={self.id}, access_token='{self.access_token}', refresh_token='{self.refresh_token}', user_id={self.user_id})"

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    date = Column(Float)
    total_amount = Column(Float)
    status = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order(id={self.id}, date={self.date}, total_amount={self.total_amount}, status={self.status})>"


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    image = Column(String)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, quantity={self.quantity})>"


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    unit_price = Column(Float)
    discount = Column(Float)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, quantity={self.quantity}, unit_price={self.unit_price}, discount={self.discount})>"


class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User")

    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id})>"


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    amount = Column(Float)
    order_id = Column(Integer, ForeignKey('orders.id'))

    order = relationship("Order")

    def __repr__(self):
        return f"<Payment(id={self.id}, type={self.type}, amount={self.amount})>"


class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    last_updated = Column(Float)

    product = relationship("Product")

    def __repr__(self):
        return f"<Inventory(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, last_updated={self.last_updated})>"
