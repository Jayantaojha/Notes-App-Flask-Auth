from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

# Initialize SQLAlchemy object
db = SQLAlchemy()
DB_NAME = "database.db" # Name of the SQLite database file


def create_app():
    app = Flask(__name__)  # create a Flask application instance

    # set up application configuration
    app.config['SECRET_KEY'] = 'Shreya Bandyopadhyay'  # secret key for session management
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #database URI for SQLite


    # Initialize the SQLAlchemy object with the Flask app
    db.init_app(app)

    # import and register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    from .models import User, Note

    # create database tables
    with app.app_context():
        db.create_all()  # create all tables in the database
    

    # set up flask login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # Redirect to login page if a user is not logged in
    login_manager.init_app(app) # Initialize the login manager with the Flask app


    # User loader callback to retrieve a user by ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # Query the user by their ID

    return app


def create_database(app):
    # check if the database file exits
    if not path.exists('website/' + DB_NAME):
        # if not, create the database and tables
        db.create_all(app=app)
        print('Created Database!')