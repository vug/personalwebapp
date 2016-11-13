from datetime import datetime
import os
import random

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_required, logout_user, login_user
from flask_misaka import Misaka, markdown
from flask_sqlalchemy import SQLAlchemy

static_pages = {'about.html', 'projects.html', 'music.html', 'research.html'}

app = Flask(__name__)
Misaka(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # sqlite://<nohostname>/<path>
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('secret.py', silent=True)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # redirect to this when arrived a login_required view without logged in


class User(db.Model):
    """A PersonalWebApp user model.

    This model is both to store any kind of user related information, and to serve as Flask-Login user. i.e. it has
    fields such as fullname and created_at, and it has the functions needed to be implemented to be a
    flask_login.UserMixin (which is not explicitly inherited) such as is_anonymous and get_id."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    fullname = db.Column(db.String(80), unique=True)
    created_at = db.Column('created_at', db.DateTime)

    def __init__(self, email, password, fullname):
        self.email = email
        self.password = password
        self.fullname = fullname
        self.created_at = datetime.utcnow()

    def is_authenticated(self):
        """Return True to indicate that the user provided valid credentials."""
        return True

    def is_active(self):
        """Return True to indicate that the user is active (registered)."""
        return True

    def is_anonymous(self):
        """Return False to indicate that the user is not anonymous."""
        return False

    def get_id(self):
        """Return a unicode that uniquely identifies this user."""
        return u'{}'.format(self.id)

    def __repr__(self):
        return '<User %r>' % self.email


def rnd_clr():
    colors = ['#9ad3de', 'rgb(252,123,52)', '#3fb0ac', '#fae596', '#dbe9d8', '#f2efe8', '#fccdd3']
    return random.choice(colors)


@app.route('/<name>')
def static_page(name):
    if name in static_pages:
        return render_template(name, bg_color=rnd_clr())
    else:
        return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('home.html', bg_color=rnd_clr())


@app.route('/blog/')
def blog():
    post_list = os.listdir('posts')
    return render_template('blog_list.html', post_list=post_list)


@app.route('/blog/<post>')
def blog_post(post):
    with open(os.path.join('posts', post), 'rt') as f:
        md_text = f.read()
    html = markdown(md_text, fenced_code=True, math=True)
    first_three_lines = md_text.split('\n')[:3]
    title, date, tags = [line.split('(')[1][:-1] for line in first_three_lines]
    tags = tags.split(',')
    # https://flask-misaka.readthedocs.io/en/latest/
    # http://misaka.61924.nl/#
    return render_template('blog_post.html', post=html, date=date, tags=tags)


@login_manager.user_loader
def load_user(user_id):
    """Get the User object given the user_id stored in the session.

    This is a callback function to reload the user object from the user ID stored in the session."""
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user is not None and user.password == password:
            login_user(user, remember=True)
            fullname = user.fullname
            redirect_url = request.args.get('next')
            html = 'Logged in as email: {}, fullname: {}<br><a href="/">Home</a> '.format(email, fullname)
            if redirect_url:
                html += '<a href="{}">Redirect</a>'.format(redirect_url)
            return html
        else:
            flash('Username or Password is invalid', 'error')
            return redirect(url_for('login'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return 'Logged out'


@app.route('/admin')
@login_required
def admin():
    return 'Welcome to admin page. You must be a PersonalWebApp user.'
