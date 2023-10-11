#!/usr/bin/env python3
from gui import dashboard
from scada import modbus_master

def create_app(app):
    """
    Sets up flask app to work with sqlalchemy database
    Creates users in database for login
    """
    from SFclasses.user_handler import db
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///login.db"
    from SFclasses.user_handler import generate_random_cookie
    app.secret_key = generate_random_cookie() # should be randomized
    db.init_app(app)
    from SFclasses.user_handler import create_users
    with app.app_context():
        db.create_all()
        create_users()

def main():
    modbus_master.start_client()
    dashboard.app.run(debug=True)

if __name__ == "__main__":
    main()
