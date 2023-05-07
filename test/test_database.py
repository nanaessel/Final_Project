# import unittest

import unittest
import sys
import os

# # Add the current and parent directory of this file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'service')))

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from domains.model import Base, User

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///test.db')
        self.db_session = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(bind=self.engine)

    def tearDown(self):
        self.db_session.remove()
        Base.metadata.drop_all(bind=self.engine)

    def test_add_user(self):
        user = User(name='John', email='john@example.com')
        self.db_session.add(user)
        self.db_session.commit()
        result = self.db_session.query(User).all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'John')
        self.assertEqual(result[0].email, 'john@example.com')
