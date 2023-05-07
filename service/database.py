from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from ..domains.model import Base


engine = create_engine('sqlite:///RREP.db')
Base.metadata.bind = engine

# Creates the session
session = scoped_session(sessionmaker(bind=engine))


def get_session():
    return session