"""
This module has create_app function that creates a PersonalWebApp Flask app according to application factory pattern.
"""
from flask import Flask

from extensions import login_manager, misaka, db
from views import static_pages, blog, login, simple_routes, tags_api


def create_app(config=None):
    """Return a Flask application according to application factory design pattern function.

    Create app object. Configure it. Initialize Flask extensions. Register Blueprints.

    :type config: dict
    :param config: Additional configuration that'll override default values
    """
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # sqlite://<nohostname>/<path>
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config.from_pyfile('secret.py', silent=True)
    if config is not None:
        app.config.update(config)

    misaka.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    app.register_blueprint(login)
    app.register_blueprint(static_pages)
    app.register_blueprint(blog, url_prefix='/blog')
    app.register_blueprint(simple_routes)
    app.register_blueprint(tags_api, url_prefix='/blog')

    return app
