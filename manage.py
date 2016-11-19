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
def gen_secret():
    """Generate a secret_key for Flask-Login security and write it into secret.py."""
    import os
    import binascii

    key = binascii.hexlify(os.urandom(24))
    with open('secret.py', 'wt') as f:
        f.write("SECRET_KEY = '{}'".format(key))


@manager.command
def create_db():
    """Create database and its schema. Add post states 'draft' and 'published'"""
    db.create_all()

    from models import PostState
    PostState.query.delete()
    db.session.add(PostState('draft'))
    db.session.add(PostState('published'))
    db.session.commit()

    print('Database schema and, "draft" and "published" blog post states have been created. '
          'You can use populate_db command to populate it with the first post and an example draft post. '
          'Also the create_user command to create admin users who can write blog posts.')


@manager.option('--email', help='email of the user')
@manager.option('--password', help='password of the user')
@manager.option('--fullname', help='fullname of the user')
@manager.option('--timezone', help='timezone of user as integer N in UTC+N', type=int)
def create_user(email, password, fullname, timezone):
    """Insert a new PersonalWebApp User into database."""
    user = User(email, password, fullname, timezone)
    db.session.add(user)
    db.session.commit()
    print('New user with email address "{}" has been generated'.format(email))


FIRST_POST = '''
I decided to make a personal website with the goal that it'll help me to organize my mind and collect my projects at a single location. I wanted to have a blog too. It is a productive way of dealing with tough times, provides focus and allows keeping track of self.

I found this as an opportunity (or excuse) to write my own blogging software. At work, I learned much about web development and finally it is time to apply that knowledge to other aspects of my life. ^_^

Writing your own web app just to publish a few blog posts is super unnecessary and looks counter-productive. There are content management systems such as [Wordpress](https://wordpress.org/), [PageKit](https://pagekit.com/) which do the job perfectly. But, I am a theoretical physicist. We are one of the most impractical kind of people out there. I'm totally not surprised with my decision.

<blockquote width="300px" class="twitter-tweet tw-align-center" data-lang="en"><p lang="en" dir="ltr">It&#39;s basically a rite of passage <a href="https://t.co/sP2x1czQBK">pic.twitter.com/sP2x1czQBK</a></p>&mdash; The Practical Dev (@ThePracticalDev) <a href="https://twitter.com/ThePracticalDev/status/799634252946087936">November 18, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

I rented an [EC2](https://aws.amazon.com/ec2/) instance on AWS and there I am running a [Flask](http://flask.pocoo.org/) web application.  It doesn't help much about the static parts of the website (about, music etc. sections), actually it makes it harder to serve them. :-) But allows me to dynamically write, store, edit blog posts.

Later I'll go into the details of how different parts are implemented. For now you can just check the source code of the website on its [GitHub repository](https://github.com/vug/personalwebapp).

Hope I'll have enough patience and persistence to write continuously. Laylay...
'''


@manager.command
def populate_db():
    """Add 'personalwebapp' tag, first post to database."""
    from models import Post, Tag, post_to_tag
    Post.query.delete()
    Tag.query.delete()
    db.session.execute(post_to_tag.delete())

    personalwebapp = Tag(name='personalwebapp')
    db.session.add(personalwebapp)

    post = Post(title='Hello PersonalWebApp!', content=FIRST_POST, author_id=1)
    post.tags.append(personalwebapp)
    post.state_id = 2
    from datetime import datetime
    post.published_at = datetime.utcnow()
    post.url = 'hello_personal_webapp'
    db.session.add(post)

    post = Post(title='Example Draft Post', content='This is the first draft. I\'ll finish it later.', author_id=1)
    post.url = 'example_draft_post'
    db.session.add(post)

    db.session.commit()

    print('"personalwebapp" tag'
          'and "Hello PersonalWebApp!" published post and "Example Draft Post" draft post have been generated.')


if __name__ == '__main__':
    manager.run()
