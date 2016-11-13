import unittest

from factory import create_app
from extensions import db
from models import User


class MyTest(unittest.TestCase):
    def setUp(self):
        sqlite_in_memory_uri = 'sqlite://'
        config = {'SQLALCHEMY_DATABASE_URI': sqlite_in_memory_uri,
                  'TESTING': True}
        app = create_app(config)

        self.test_user_email = 'tester@test_users.com'
        self.test_user_password = 'password'

        with app.app_context():
            db.create_all()
            self.test_user = User(self.test_user_email, self.test_user_password, 'Mr. Tester')
            db.session.add(self.test_user)
            db.session.commit()

        self.app = app.test_client()
        self.get_context = app.app_context

    def tearDown(self):
        with self.get_context():
            db.drop_all()

    def login(self):
        rv = self.app.post('/login',
                           data={'email': self.test_user_email, 'password': self.test_user_password},
                           follow_redirects=True)
        return rv

    def logout(self):
        self.app.get('/logout')


    def test_can_access_static_pages(self):
        rv = self.app.get('/')
        assert b'home_page' in rv.data

        rv = self.app.get('/about.html')
        assert b'about_page' in rv.data

        rv = self.app.get('/music.html')
        assert b'music_page' in rv.data

        rv = self.app.get('/projects.html')
        assert b'projects_page' in rv.data

    def test_can_access_login(self):
        rv = self.app.get('/login')
        assert b'login_page' in rv.data

        rv = self.app.get('/logout')
        assert b'logout_page' in rv.data

    def test_can_access_blog(self):
        rv = self.app.get('/blog/')
        assert b'blog_posts_list_page' in rv.data


if __name__ == '__main__':
    unittest.main()
