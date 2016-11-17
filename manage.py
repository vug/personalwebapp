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


FIRST_POST = '''
I decided to make a personal website with the goal that it'll help me to organize my mind and collect my projects at a single location. I wanted to have a blog too. It is a productive way of dealing with tough times, provides focus and allows keeping track of self.

I found this as an opportunity (or excuse) to write my own blogging software. At work, I learned much about web development and finally it is time to apply that knowledge to other aspects of my life. ^_^

Writing your own web app just to publish a few blog posts is super unnecessary and looks counter-productive. There are content management systems such as [Wordpress](https://wordpress.org/), [PageKit](https://pagekit.com/) which do the job perfectly. But, I am a theoretical physicist. We are one of the most impractical kind of people out there. I'm totally not surprised with my decision.

I rented an [EC2](https://aws.amazon.com/ec2/) instance on AWS and there I am running a [Flask](http://flask.pocoo.org/) web application.  It doesn't help much about the static parts of the website (about, music etc. sections), actually it makes it harder to serve them. :-) But allows me to dynamically write, store, edit blog posts.

Later I'll go into the details of how different parts are implemented. For now you can just check the source code of the website on its [GitHub repository](https://github.com/vug/personalwebapp).

Hope I'll have enough patience and persistence to write continuously. Laylay...
'''

@manager.command
def populate_db():
    from models import PostState
    PostState.query.delete()
    db.session.add(PostState('draft'))
    db.session.add(PostState('published'))
    db.session.commit()

    from models import Post, Tag, posts_to_tags
    from datetime import datetime
    Post.query.delete()
    Tag.query.delete()
    db.session.execute(posts_to_tags.delete())

    python, politics, programming, turkish = [Tag(tname) for tname in ['python', 'politics', 'programming', 'turkish']]
    for tag in [python, politics, programming, turkish]:
        db.session.add(tag)

    post = Post(title='Hello PersonalWebApp!', content=FIRST_POST, author_id=2)
    post.tags.append(python)
    post.tags.append(programming)
    post.state = 2
    post.url = 'hello_personal_webapp'
    db.session.add(post)

    post = Post(title='Highlights From This Week', content='This week was so busy.', author_id=2)
    post.tags.append(python)
    post.tags.append(politics)
    post.url = 'highlights_from_this_week'
    db.session.add(post)

    db.session.commit()

    from models import User
    User.query.delete()
    user = User('admin@email.com', 'password', 'Ad Min')
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
