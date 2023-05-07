
import unittest
from unittest.mock import patch
from flask_login import UserMixin
from app import app, session, login_manager
from ..service.auth_service import get_user_by_email, check_user_password
from ..service.auth_service import login, logout, is_authenticated

# Define a dummy User class that implements the UserMixin interface
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Use the login_manager to load the user object from the user id
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Define a test case that tests the login function
class LoginTestCase(unittest.TestCase):
    def setUp(self):
        # Configure the Flask app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'test-secret-key'
        self.app = app.test_client()
        session.create_all()

    def tearDown(self):
        session.session.remove()
        session.drop_all()

    @patch('users_service.get_user_by_email')
    @patch('users_service.check_user_password')
    @patch('flask_login.login_user')
    def test_login_success(self, mock_login_user, mock_check_user_password, mock_get_user_by_email):
        # Set up mock user data
        email = 'test@example.com'
        password = 'password'
        user_id = 1
        mock_user = User(user_id)

        # Mock the user service to return a user
        mock_get_user_by_email.return_value = mock_user
        mock_check_user_password.return_value = True

        # Call the login function
        result = login(email, password, remember=False)

        # Verify that the function returned True and that login_user was called
        self.assertTrue(result)
        mock_login_user.assert_called_once_with(mock_user)

    @patch('users_service.get_user_by_email')
    @patch('users_service.check_user_password')
    @patch('flask_login.login_user')
    def test_login_failure(self, mock_login_user, mock_check_user_password, mock_get_user_by_email):
        # Set up mock user data
        email = 'test@example.com'
        password = 'password'
        user_id = 1
        mock_user = User(user_id)

        # Mock the user service to return a user, but with an incorrect password
        mock_get_user_by_email.return_value = mock_user
        mock_check_user_password.return_value = False

        # Call the login function
        result = login(email, password, remember=False)

        # Verify that the function returned False and that login_user was not called
        self.assertFalse(result)
        mock_login_user.assert_not_called()

    def test_logout(self):
        # Call the logout function
        logout()

        # Verify that the current user is not authenticated
        self.assertFalse(is_authenticated())

if __name__ == '__main__':
    unittest.main()
