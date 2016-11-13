from flask_script import Manager

from app import app, db

manager = Manager(app)


@manager.command
def create_db():
    db.create_all()


@manager.option('--email', help='email of the user')
@manager.option('--password', help='password of the user')
@manager.option('--fullname', help='fullname of the user')
def create_user(email, password, fullname):
    user = app.User(email, password, fullname)
    db.session.add(user)
    db.session.commit()
    print('New user with email address "{}" has been generated'.format(email))


if __name__ == '__main__':
    manager.run()
