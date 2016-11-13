"""
This module has create_app function that creates a PersonalWebApp Flask app according to application factory pattern.
"""
from flask import Flask

from extensions import login_manager, misaka, db
from views import static_pages, blog, login, simple_routes


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # sqlite://<nohostname>/<path>
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_pyfile('secret.py', silent=True)

    misaka.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    app.register_blueprint(login)
    app.register_blueprint(static_pages)
    app.register_blueprint(blog, url_prefix='/blog')
    app.register_blueprint(simple_routes)

    return app
