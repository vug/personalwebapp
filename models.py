"""
Database models for the app.
"""
from datetime import datetime

from extensions import db


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
