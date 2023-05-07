# registration_service.py
from werkzeug.security import generate_password_hash
from database import Users, session


def register_user(fullname, phonenumber, usertype, emailaddress, password):
    # hash the password
    hashed_password = generate_password_hash(password, method='sha256')

    # create a new user
    new_user = Users(FullName=fullname, PhoneNumber=phonenumber, UserType=usertype, EmailAddress=emailaddress, Password=hashed_password)

    # add the new user to the database
    session.add(new_user)
    session.commit()
