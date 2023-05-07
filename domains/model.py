# from sqlalchemy.orm import Session

# from entities import Product, Reserve, Users

# def get_products(db: Session):
#     return db.query(Product).all()


# def get_product_by_name(db: Session, name: str):
#     return db.query(Product).filter(Product.ProductName == name).first()


# def get_reserves(db: Session):
#     return db.query(Reserve).all()


# def get_users(db: Session):
#     return db.query(Users).all()


# def get_user_by_phone_number(db: Session, phone_number: str):
#     return db.query(Users).filter(Users.PhoneNumber == phone_number).first()


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
