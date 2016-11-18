import unittest

from .base import TestBase
from extensions import db
from models import User


class TestRoutes(TestBase):
    def test_can_access_static_pages(self):
        rv = self.app.get('/')
        assert b'home_page' in rv.data

        rv = self.app.get('/about.html')
        assert b'about_page' in rv.data

        rv = self.app.get('/music.html')
        assert b'music_page' in rv.data

        rv = self.app.get('/projects.html')
        assert b'projects_page' in rv.data

    def test_attempt_nonexisting_url(self):
        rv = self.app.get('/noroutewiththisurl')
        assert rv.status_code == 404

    def test_can_access_login_related_pages(self):
        rv = self.app.get('/login')
        assert b'login_page' in rv.data

        rv = self.app.get('/logout')
        assert b'logout_page' in rv.data

    def test_incorrect_credentials(self):
        rv = self.login('hacker', '123456')
        assert b'Username or Password is invalid' in rv.data

    def test_anonymous_cannot_visit_admin(self):
        self.logout()
        rv = self.app.get('/admin')
        assert b'admin_page' not in rv.data

    def test_anonymous_visit_to_protected_page_redirects_to_login(self):
        protected_page = '/admin'
        rv = self.app.get(protected_page, follow_redirects=True)
        assert b'login_page' in rv.data
        assert b'Please log in to access this page.' in rv.data

    def test_user_can_login(self):
        rv = self.login()
        assert b'Logged in as' in rv.data

    def test_user_can_visit_admin(self):
        self.login()
        rv = self.app.get('/admin')
        assert b'admin_page' in rv.data

    def test_protected_page_redirect_appears_after_login(self):
        protected_page = 'admin'
        rv = self.login(redirect=protected_page)
        assert b'Redirect' in rv.data
        assert 'href="/{}"'.format(protected_page).encode('utf-8') in rv.data

    def test_db_query_on_user(self):
        with self.get_context():
            assert self.test_user_email == db.session.query(User).get(1).email
            assert self.test_user_email == User.query.get(1).email


if __name__ == '__main__':
    unittest.main()
