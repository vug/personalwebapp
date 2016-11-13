from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_required, logout_user, login_user

from extensions import login_manager, misaka, db
from models import User
from views import static_pages, blog


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # sqlite://<nohostname>/<path>
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('secret.py', silent=True)

misaka.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'  # redirect to this when arrived a login_required view without logged in
db.init_app(app)

app.register_blueprint(static_pages)
app.register_blueprint(blog, url_prefix='/blog')


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
    return 'Logged out<br><a href="/">Home</a>'


@app.route('/admin')
@login_required
def admin():
    return 'Welcome to admin page. You must be a PersonalWebApp user.'
