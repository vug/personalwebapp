from datetime import datetime

from extensions import db


posts_to_tags = db.Table('posts_to_tags',
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
    view_count = db.Column(db.Integer, default=0)
    state = db.Column(db.Integer, db.ForeignKey('state.id'))
    tags = db.relationship('Tag', secondary=posts_to_tags, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, content, author_id):
        self.title = title
        self.url = 'random_url_' + generate_random_string()
        self.content = content
        self.author_id = author_id
        self.created_at = datetime.utcnow()
        self.state = 1

    def set_url_from_title(self):
        self.url = self.title.lower().replace(' ', '_')


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


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

