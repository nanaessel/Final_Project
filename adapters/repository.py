from abc import ABC, abstractmethod
from typing import List, Tuple

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .orm import Users, Product, Reserve, Category


class AbstractRepository(ABC):
    """An abstract base class for a repository that provides
    methods for CRUD operations on the data model objects.
    """

    @abstractmethod
    def add_user(self, user: Users):
        """Add a new user to the repository."""

    @abstractmethod
    def get_user_by_email(self, email: str) -> Users:
        """Get a user from the repository by their email address."""

    @abstractmethod
    def add_product(self, product: Product):
        """Add a new product to the repository."""

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Product:
        """Get a product from the repository by its ID."""

    @abstractmethod
    def get_products_by_category(self, category_name: str) -> List[Product]:
        """Get all products from the repository that belong to the given category."""

    @abstractmethod
    def add_reserve(self, reserve: Reserve):
        """Add a new reserve to the repository."""

    @abstractmethod
    def get_reserve_by_id(self, reserve_id: int) -> Reserve:
        """Get a reserve from the repository by its ID."""

    @abstractmethod
    def get_reserves_by_user(self, user_id: int) -> List[Reserve]:
        """Get all reserves from the repository that belong to the given user."""


class SqlAlchemyRepository(AbstractRepository):
    """A concrete implementation of the repository that uses SQLAlchemy
    as the ORM to interact with a SQLite database.
    """

    def __init__(self, session: Session):
        """Initialize the repository with a SQLAlchemy session."""
        self._session = session

    def add_user(self, user: Users):
        """Add a new user to the repository."""
        self._session.add(user)
        self._session.commit()

    def get_user_by_email(self, email: str) -> Users:
        """Get a user from the repository by their email address."""
        return self._session.query(Users).filter_by(EmailAddress=email).first()

    def add_product(self, product: Product):
        """Add a new product to the repository."""
        self._session.add(product)
        self._session.commit()

    def get_product_by_id(self, product_id: int) -> Product:
        """Get a product from the repository by its ID."""
        return self._session.query(Product).filter_by(ID=product_id).first()

    def get_products_by_category(self, category_name: str) -> List[Product]:
        """Get all products from the repository that belong to the given category."""
        return self._session.query(Product).filter_by(Category=category_name).all()

    def add_reserve(self, reserve: Reserve):
        """Add a new reserve to the repository."""
        self._session.add(reserve)
        self._session.commit()

    def get_reserve_by_id(self, reserve_id: int) -> Reserve:
        """Get a reserve from the repository by its ID."""
        return self._session.query(Reserve).filter_by(ID=reserve_id).first()

    def get_reserves_by_user(self, user_id: int) -> List[Reserve]:
        """Get all reserves from the repository that belong to the given user."""
        return self._session.query(Reserve).filter_by(UserID=user_id).all()

    def add_category(self, category: Category):
        """Add a new category to the repository."""
        self._session.add(category)
        self._session.commit()

    def get_all_categories(self) -> List[Category]:
        """Get all categories from the repository."""
        return self._session.query(Category).all()

    def delete_category(self, category_name: str):
        """Delete a category from the repository."""
        category = self._session.query(Category).filter_by(Name=category_name).first()
        self._session.delete(category)
        self._session.commit()

    def update_category_name(self, old_name: str, new_name: str):
        """Update the name of a category in the repository."""
        category = self._session.query(Category).filter_by(Name=old_name).first()
        category.Name = new_name
        self._session.commit()
       
