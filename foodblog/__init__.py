from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
# from flask_wtf.csrf import CSRFProtect



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',
                                            'default_fallback_key')

uri = os.environ['DATABASE_URL']
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri

# app.config['SECRET_KEY'] = '4567bfpahg309bndh357hfpsba245'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/foodblog'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'dark'
# csrf = CSRFProtect(app)

from foodblog import routes

