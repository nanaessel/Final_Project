from datetime import datetime
from typing import Optional
from dataclasses import dataclass


class Command:
    pass


@dataclass
class CreateUser(Command):
    full_name: str
    phone_number: str
    user_type: str
    email_address: str
    password: str
    created_date: Optional[datetime] = None


@dataclass
class CreateProduct(Command):
    product_name: str
    product_description: str
    price: int
    category: str
    landlord_id: int
    created_date: Optional[datetime] = None


@dataclass
class ReserveProduct(Command):
    product_name: str
    receiver_name: str
    phone_number: str
    address: str
    created_date: Optional[datetime] = None


@dataclass
class CreateCategory(Command):
    name: str
