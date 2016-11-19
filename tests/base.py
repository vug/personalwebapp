import unittest

from factory import create_app
from extensions import db
from models import User, PostState


class TestBase(unittest.TestCase):
    def setUp(self):
        sqlite_in_memory_uri = 'sqlite://'
        config = {'SQLALCHEMY_DATABASE_URI': sqlite_in_memory_uri,
                  'TESTING': True,
                  'WTF_CSRF_ENABLED': False}
        app = create_app(config)

        self.test_user_email = 'tester@test_users.com'
        self.test_user_password = 'password'

        with app.app_context():
            db.create_all()
            self.test_user = User(self.test_user_email, self.test_user_password, 'Mr. Tester', timezone=-5)
            db.session.add(self.test_user)
            db.session.add(PostState(name='draft'))
            db.session.add(PostState(name='published'))
            db.session.commit()

        self.app = app.test_client()
        self.get_context = app.app_context

    def tearDown(self):
        with self.get_context():
            db.drop_all()

    def login(self, email=None, password=None, redirect=None):
        if email is None:
            email = self.test_user_email
        if password is None:
            password = self.test_user_password
        login_url = '/login'
        if redirect:
            login_url += '?next=%2F{}'.format(redirect)
        rv = self.app.post(login_url,
                           data={'email': email, 'password': password},
                           follow_redirects=True)
        return rv

    def logout(self):
        self.app.get('/logout')

    def get_test_user(self):
        """Get a user object reconciled with session.

        Any call to an expired model requires database hit. Calls to self.test_user would cause DetachedInstanceError:
        "Instance <User at ...> is not bound to a Session". Because the session in which test_user was created no
        longer exists. To continue working with detached object, reconcile it with the current session.

        from: https://flask-webtest.readthedocs.io/
        """
        with self.get_context():
            test_user = db.session.merge(self.test_user)
            return test_user
