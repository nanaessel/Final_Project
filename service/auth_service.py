from flask_login import login_user, logout_user, current_user
from users_service import get_user_by_email, check_user_password


def login(email, password, remember):
    user = get_user_by_email(email)
    if user and check_user_password(user, password):
        login_user(user, remember=remember)
        return True
    return False


def logout():
    logout_user()


def is_authenticated():
    return current_user.is_authenticated
