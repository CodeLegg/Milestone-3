from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_wtf.csrf import CSRFProtect



app = Flask(__name__)
app.config['SECRET_KEY'] = '4567bfpahg309bndh357hfpsba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'dark'
csrf = CSRFProtect(app)

from foodblog import routes

