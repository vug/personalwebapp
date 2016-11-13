from flask import Flask
from flask_login import login_required

from extensions import login_manager, misaka, db
from views import static_pages, blog, login


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


@app.route('/admin')
@login_required
def admin():
    return 'Welcome to admin page. You must be a PersonalWebApp user.'
