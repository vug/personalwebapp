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
    published_at = db.Column(db.DateTime)
    edited_at = db.Column(db.DateTime)
    view_count = db.Column(db.Integer, default=0)
    status = db.Column(db.Text)
    tags = db.relationship('Tag', secondary=posts_to_tags, backref=db.backref('pages', lazy='dynamic'))

    def __init__(self, title, content, author_id):
        self.title = title
        self.url = title.lower().replace(' ', '_')
        self.content = content
        self.author_id = author_id


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

