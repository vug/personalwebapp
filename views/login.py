"""
This Blueprint gives the ability of user logins, and login_required functionality using Flask-Login extension.
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, logout_user, login_user

from extensions import login_manager
from models import User

login = Blueprint('login', __name__)

login_manager.login_view = 'login.login_page'  # redirect to this when arrived a login_required view without logged in


@login_manager.user_loader
def load_user(user_id):
    """Get the User object given the user_id stored in the session.

    This is a callback function to reload the user object from the user ID stored in the session.

    :rtype: User
    :return: A User if user_id exists, else None."""
    return User.query.get(int(user_id))


@login.route('/login', methods=['GET', 'POST'])
def login_page():
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
            return redirect(url_for('login.login_page'))


@login.route("/logout")
@login_required
def logout_page():
    logout_user()
    return 'Logged out<br><a href="/">Home</a>'
