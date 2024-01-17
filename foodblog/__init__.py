from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

# from flask_wtf.csrf import CSRFProtect



app = Flask(__name__)
app.config['SECRET_KEY'] = '4567bfpahg309bndh357hfpsba245'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL' , 'postgres://hkuzcfrwsqfxef:8e058f0d64be67a32104dc79dd25cd116c882c0beb3a2715bbc693992547f7f2@ec2-54-73-22-169.eu-west-1.compute.amazonaws.com:5432/dv09pn3hrk504')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/foodblog'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'dark'
# csrf = CSRFProtect(app)

from foodblog import routes



