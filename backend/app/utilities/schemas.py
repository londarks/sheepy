from typing import List, Union
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    address: str
    email: str
    phone: str
    password: str

class Login(BaseModel):
    email: str
    phone: str