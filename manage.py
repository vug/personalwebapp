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
        f.write('SECRET_KEY = {}'.format(key))


if __name__ == '__main__':
    manager.run()
