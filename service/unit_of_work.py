from __future__ import annotations
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from contextlib import contextmanager

from domain import model
from domain.commands import Command
from domain.events import Event
from domain.messagebus import MessageBus


class AbstractUnitOfWork:
    def __enter__(self) -> AbstractUnitOfWork:
        raise NotImplementedError

    def __exit__(self, *args):
        raise NotImplementedError

    def products(self) -> Repository[model.Product]:
        raise NotImplementedError

    def categories(self) -> Repository[model.Category]:
        raise NotImplementedError

    def users(self) -> Repository[model.Users]:
        raise NotImplementedError

    def reserves(self) -> Repository[model.Reserve]:
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory, bus: MessageBus):
        self.session_factory = session_factory
        self.bus = bus

    def __enter__(self):
        self.session = self.session_factory()
        self.products_repo = SqlAlchemyRepository[self.session, model.Product]
        self.categories_repo = SqlAlchemyRepository[self.session, model.Category]
        self.users_repo = SqlAlchemyRepository[self.session, model.Users]
        self.reserves_repo = SqlAlchemyRepository[self.session, model.Reserve]
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()
        self.bus.publish(self.collect_new_events())

    def collect_new_events(self) -> List[Event]:
        return self.bus.events

    def rollback(self):
        self.session.rollback()

    def products(self) -> Repository[model.Product]:
        return self.products_repo

    def categories(self) -> Repository[model.Category]:
        return self.categories_repo

    def users(self) -> Repository[model.Users]:
        return self.users_repo

    def reserves(self) -> Repository[model.Reserve]:
        return self.reserves_repo


class Repository:
    def __getitem__(self, id) -> model.Product:
        raise NotImplementedError

    def add(self, product: model.Product):
        raise NotImplementedError

    def update(self, product: model.Product):
        raise NotImplementedError

    def delete(self, product: model.Product):
        raise NotImplementedError

    def list(self) -> List[model.Product]:
        raise NotImplementedError


class SqlAlchemyRepository(Repository):
    def __init__(self, session: Session, entity: type[model.Product]):
        self.session = session
        self.entity = entity

    def __getitem__(self, id) -> model.Product:
        return self.session.query(self.entity).filter_by(ID=id).one()

    def add(self, entity: model.Product):
        self.session.add(entity)

    def update(self, entity: model.Product):
        self.session.add(entity)

    def delete(self, entity: model.Product):
        self.session.delete(entity)

    def list(self) -> List[model.Product]:
        return self.session.query(self.entity).all()


@contextmanager
def unit_of_work(session_factory):
    bus = MessageBus()
    uow = SqlAlchemyUnitOfWork(session_factory, bus)
    try:
        yield uow
        uow.commit()
    except:
        uow.rollback()
        raise
