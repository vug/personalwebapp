from flask_login import LoginManager
from flask_misaka import Misaka
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
misaka = Misaka()
