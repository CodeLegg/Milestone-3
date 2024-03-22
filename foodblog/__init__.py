from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "default_fallback_key")

# uri = os.environ["DATABASE_URL"]
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)
# app.config["SQLALCHEMY_DATABASE_URI"] = uri

# # Check and modify the URI if necessary
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "dark"

from foodblog import routes
