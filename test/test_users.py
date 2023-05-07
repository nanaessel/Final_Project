import sys
import os

# Add the parent directory of this file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Users, Base


class TestUsers(unittest.TestCase):
    
    def setUp(self):
        # Create an in-memory SQLite database and connect to it
        engine = create_engine('sqlite:///:memory:', echo=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)
        
    def test_create_user(self):
        # Create a new user
        user = Users(
            FullName='John Doe',
            PhoneNumber='555-1234',
            UserType='Customer',
            EmailAddress='johndoe@example.com',
            Password='password123'
        )
        
        # Add the user to the session and commit the transaction
        self.session.add(user)
        self.session.commit()
        
        # Retrieve the user from the database
        retrieved_user = self.session.query(Users).filter_by(PhoneNumber='555-1234').first()
        
        # Check that the user was retrieved successfully
        self.assertEqual(retrieved_user.FullName, 'John Doe')
        self.assertEqual(retrieved_user.UserType, 'Customer')
        
    def tearDown(self):
        # Roll back the transaction and close the session
        self.session.rollback()
        self.session.close()

if __name__ == '__main__':
    unittest.main()
