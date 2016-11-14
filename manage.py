"""
Flask-Script Manager commands to be run from command line. Examples

python manager.py --help
python manager.py create_db
"""
from flask_script import Manager

from extensions import db
from models import User

from factory import create_app

manager = Manager(create_app())


@manager.command
def create_db():
    """Create database and its schema."""
    db.create_all()


@manager.option('--email', help='email of the user')
@manager.option('--password', help='password of the user')
@manager.option('--fullname', help='fullname of the user')
def create_user(email, password, fullname):
    """Insert a new PersonalWebApp User into database."""
    user = User(email, password, fullname)
    db.session.add(user)
    db.session.commit()
    print('New user with email address "{}" has been generated'.format(email))


@manager.command
def gen_secret():
    """Generate a secret_key for Flask-Login security and write it into secret.py."""
    import os
    import binascii

    key = binascii.hexlify(os.urandom(24))
    with open('secret.py', 'wt') as f:
        f.write("SECRET_KEY = '{}'".format(key))


@manager.command
def populate_db():
    from models import Post, Tag, posts_to_tags
    from datetime import datetime
    Post.query.delete()
    Tag.query.delete()
    db.session.execute(posts_to_tags.delete())

    python, politics, programming, turkish = [Tag(tname) for tname in ['python', 'politics', 'programming', 'turkish']]
    for tag in [python, politics, programming, turkish]:
        db.session.add(tag)

    post = Post(title='Hello PersonalWebApp', content='This is my first post. Welcome to my site', author_id=2)
    post.published_at = datetime.utcnow()
    post.tags.append(python)
    post.tags.append(programming)
    db.session.add(post)

    post = Post(title='Highlights From This Week', content='This week was so busy.', author_id=2)
    post.published_at = datetime.utcnow()
    post.tags.append(python)
    post.tags.append(politics)
    db.session.add(post)

    db.session.commit()

    from models import User
    user = User('admin@email.com', 'password', 'Ad Min')
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
