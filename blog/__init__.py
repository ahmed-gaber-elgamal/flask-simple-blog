from flask import Flask
from blog.core.views import core
from blog.error_pages.handlers import error_pages
from blog.users.views import users
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager

app = Flask(__name__)
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)

########################
# DB SETUP #############
########################

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'mysecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

########################
# Login configs ########
########################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
