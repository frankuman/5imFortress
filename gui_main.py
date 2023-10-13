#!/usr/bin/env python3



def create_app(app):
    """
    Sets up flask app to work with sqlalchemy database
    Creates users in database for login
    """
    import os
    app_root = os.path.dirname(__file__)  # Assuming this code is in your main application file

    # Specify the path to the database file in the /frontend/instance directory
    db_file_path = os.path.join(app_root, 'frontend', 'instance', 'login.db')
    from frontend.helpers.user_handler import db
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file_path}"
    from frontend.helpers.user_handler import generate_random_cookie
    app.secret_key = generate_random_cookie() # should be randomized
    db.init_app(app)
    from frontend.helpers.user_handler import create_users
    with app.app_context():
        db.create_all()
        create_users()

def main():
    from scada import modbus_master
    from frontend.gui import dashboard
    modbus_master.start_client()
    dashboard.app.run()

