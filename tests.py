import unittest

from factory import create_app
from extensions import db


class MyTest(unittest.TestCase):
    def setUp(self):
        sqlite_in_memory_uri = 'sqlite://'
        config = {'SQLALCHEMY_DATABASE_URI': sqlite_in_memory_uri,
                  'TESTING': True}
        app = create_app(config)
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        pass

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
        
    def test_can_access_blog(self):
        rv = self.app.get('/blog/')
        assert b'blog_posts_list_page' in rv.data


if __name__ == '__main__':
    unittest.main()
