"""
Blog related database models such as Post, Tag, PostState.
"""
from datetime import datetime

from flask_misaka import markdown

from extensions import db


post_to_tag = db.Table('post_to_tag',
                       db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                       db.Column('post_id', db.Integer, db.ForeignKey('post.id')))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    url = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    published_at = db.Column(db.DateTime)
    edited_at = db.Column(db.DateTime)
    timezone = db.Column(db.Integer, default=0)
    state_id = db.Column(db.Integer, db.ForeignKey('post_state.id'))
    tags = db.relationship('Tag', secondary=post_to_tag, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, content, author_id, timezone):
        self.title = title
        self.url = 'random_url_' + generate_random_string()
        self.content = content
        self.author_id = author_id
        self.created_at = datetime.utcnow()
        self.state_id = 1
        self.timezone = timezone


def generate_random_string(size=32):
    import random
    import string
    choices = string.ascii_letters + string.digits
    random_characters = [random.choice(choices) for _ in range(size)]
    return ''.join(random_characters)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def serialize(self):
        """Return object data in a jsonable format."""
        return {'id': self.id, 'name': self.name}


class PostState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    posts = db.relationship('Post', backref='state', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
