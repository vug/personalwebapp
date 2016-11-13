import unittest

from factory import create_app
from extensions import db


class MyTest(unittest.TestCase):
    def setUp(self):
        sqlite_in_memory_uri = 'sqlite://'
        config = {'SQLALCHEMY_DATABASE_URI': sqlite_in_memory_uri,
                  'TESTING': True}
        app = create_app(config)
        self.app = app.test_client()  # type: Flask.flask
        with app.app_context():
            db.create_all()

    def tearDown(self):
        pass

    def test_index(self):
        rv = self.app.get('/about.html')
        assert b'about_page' in rv.data


if __name__ == '__main__':
    unittest.main()
