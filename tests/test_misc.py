import unittest

from .base import TestBase


class TestMisc(TestBase):
    def test_user_model(self):
        user = self.get_test_user()
        assert user.is_authenticated()
        assert user.is_active()
        assert not user.is_anonymous()

    def test_test_user(self):
        user = self.get_test_user()
        assert user.email == self.test_user_email
        assert user.password == self.test_user_password
