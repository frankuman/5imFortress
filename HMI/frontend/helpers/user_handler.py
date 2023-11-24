"""
Classes and functions for managing users
"""
import os
import json
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

db = SQLAlchemy()

class User(db.Model):
    """
    Users
    :param str user: username
    :param str password:  password for the user
    """
    __tablename__ = 'user'

    username = db.Column("username", db.String, primary_key=True)
    password = db.Column("password", db.String)
    accesslevel = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """
        True, as all users are active
        """
        return True

    def get_id(self):
        """
        Return the user to satisfy Flask-Login's requirements
        """
        return self.username

    def is_authenticated(self):
        """
        Return True if the user is authenticated
        """
        return self.authenticated

    def is_anonymous(self):
        """
        False, as anonymous users aren't supported
        """
        return False

class LoginForm(FlaskForm):
    """
    Form class for user login
    """
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

def create_users():
    """
    Insert all users from "credentials.json" in database
    """
    user_list = []
    password_list = []
    auth_level = []
    User.query.delete()
    with open("HMI/frontend/gui/templates/credentials.json", "r", encoding = "utf-8") as f:
        json_data = json.load(f)

    for item in json_data:
        for user in item.get("user", []):
            user_list.append(user.get("name", None))
            password_list.append(user.get("password", None))
            auth_level.append(user.get("accesslevel", None))

    for user in range(len(json_data)):
        username = user_list[user]
        password = password_list[user]
        accesslevel = auth_level[user]

        user = User(username=str(username), password=str(password), accesslevel=str(accesslevel))
        #bcrypt.generate_password_hash(password) ENCRYPT HERE

        db.session.add(user)
        db.session.commit()

def generate_random_cookie():
    """
    Generate a random cookie on login
    """
    # Define the character set for the cookie
    cookie = os.urandom(24)
    return cookie
