from werkzeug.security import generate_password_hash, check_password_hash
from database import Users, get_session


def get_user_by_id(user_id):
    session = get_session()
    return session.query(Users).filter_by(ID=user_id).first()


def get_user_by_email(email):
    session = get_session()
    return session.query(Users).filter_by(EmailAddress=email).first()


def create_user(fullname, phone_number, usertype, email, password):
    session = get_session()
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = Users(FullName=fullname, PhoneNumber=phone_number, UserType=usertype, EmailAddress=email, Password=hashed_password)
    session.add(new_user)
    session.commit()
    return new_user


def check_user_password(user, password):
    return check_password_hash(user.Password, password)
