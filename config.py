
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Set secret key
SECRET_KEY='secret'

# Set up database connection
engine = create_engine('sqlite:///RREP.db')
Base = declarative_base()
Base.metadata.bind = engine

# Create database session
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

# Teardown request
def remove_session(response_or_exc):
    session.remove()
    return response_or_exc

