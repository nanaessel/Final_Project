from datetime import datetime
from typing import Dict, Any

from domains.model import Product, Reserve, Category, Users
from domains.commands import CreateUser, CreateProduct, ReserveProduct, CreateCategory
from domains.events import ProductCreated, ProductUpdated, ProductDeleted, ReserveCreated, CategoryCreated, UserCreated


class CommandHandler:
    def handle(self, command: Any) -> Any:
        raise NotImplementedError


class CreateUserHandler(CommandHandler):
    def __init__(self, session):
        self.session = session

    def handle(self, command: CreateUser) -> UserCreated:
        user = Users(FullName=command.full_name,
                     PhoneNumber=command.phone_number,
                     UserType=command.user_type,
                     EmailAddress=command.email_address,
                     Password=command.password,
                     CreatedDate=datetime.utcnow())

        self.session.add(user)
        self.session.commit()

        return UserCreated(id=user.ID,
                           full_name=user.FullName,
                           phone_number=user.PhoneNumber,
                           user_type=user.UserType,
                           email_address=user.EmailAddress,
                           password=user.Password,
                           created_at=user.CreatedDate)


class CreateProductHandler(CommandHandler):
    def __init__(self, session):
        self.session = session

    def handle(self, command: CreateProduct) -> ProductCreated:
        product = Product(ProductName=command.product_name,
                          ProductDescription=command.product_description,
                          Price=command.price,
                          Category=command.category,
                          Landlord=command.landlord_id,
                          Date=datetime.utcnow())

        self.session.add(product)
        self.session.commit()

        return ProductCreated(id=product.ID,
                              name=product.ProductName,
                              description=product.ProductDescription,
                              price=product.Price,
                              category=product.Category,
                              landlord_id=product.Landlord,
                              created_at=product.Date)


class ReserveProductHandler(CommandHandler):
    def __init__(self, session):
        self.session = session

    def handle(self, command: ReserveProduct) -> ReserveCreated:
        reserve = Reserve(ProductName=command.product_name,
                          ReceiverName=command.receiver_name,
                          PhoneNumber=command.phone_number,
                          Address=command.address,
                          Date=datetime.utcnow())

        self.session.add(reserve)
        self.session.commit()

        return ReserveCreated(id=reserve.ID,
                              product_name=reserve.ProductName,
                              receiver_name=reserve.ReceiverName,
                              phone_number=reserve.PhoneNumber,
                              address=reserve.Address,
                              created_at=reserve.Date)


class CreateCategoryHandler(CommandHandler):
    def __init__(self, session):
        self.session = session

    def handle(self, command: CreateCategory) -> CategoryCreated:
        category = Category(Name=command.name)

        self.session.add(category)
        self.session.commit()

        return CategoryCreated(id=category.ID,
                               name=category.Name,
                               created_at=datetime.utcnow())


class EventHandler:
    def handle(self, event: Any) -> None:
        raise NotImplementedError


class ProductCreatedHandler(EventHandler):
    def __init__(self, session):
        self.session = session

    def handle(self, event: ProductCreated) -> None:
        # Handle product created event
        pass


class ProductUpdatedHandler(EventHandler):
    def __init__(self, session):
        self.session = session

    def handle(self, event: ProductUpdated) -> None:
        # Handle product updated event
        pass


class ProductDeletedHandler(EventHandler):
    def __init__(self, session):
        self.session = session

    def handle(self, event: ProductDeleted) -> None:
        # Handle product deleted event
        pass


class ReserveCreatedHandler(EventHandler):
    def __init__(self, session):
        self.session = session

   
