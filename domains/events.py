from datetime import datetime
from typing import Optional
from dataclasses import dataclass


class Event:
    pass


@dataclass
class ProductCreated(Event):
    id: int
    name: str
    description: str
    price: int
    category: str
    landlord_id: int
    created_at: Optional[datetime] = None


@dataclass
class ProductUpdated(Event):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    category: Optional[str] = None
    landlord_id: Optional[int] = None
    updated_at: Optional[datetime] = None


@dataclass
class ProductDeleted(Event):
    id: int


@dataclass
class ReserveCreated(Event):
    id: int
    product_name: str
    receiver_name: str
    phone_number: str
    address: str
    created_at: Optional[datetime] = None


@dataclass
class CategoryCreated(Event):
    id: int
    name: str
    created_at: Optional[datetime] = None


@dataclass
class UserCreated(Event):
    id: int
    full_name: str
    phone_number: str
    user_type: str
    email_address: str
    password: str
    created_at: Optional[datetime] = None
