from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',
                                            'default_fallback_key')

# uri = os.environ['DATABASE_URL']
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)
# app.config['SQLALCHEMY_DATABASE_URI'] = uri


# Replace 'your_username', 'your_password', and 'mydatabase' with your actual PostgreSQL credentials and database name
local_db_url = f"postgresql://postgres:password@localhost:5432/foodblog"

# Update the database URL based on the environment
uri = os.environ.get('DATABASE_URL', local_db_url)

# # Check and modify the URI if necessary
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)

# Set the Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = uri


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'dark'

from foodblog import routes

