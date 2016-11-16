import json

import flask

from .base import TestBase


class TestTagApi(TestBase):
    def test_getting_all_tags_when_there_are_no_tags(self):
        response = self.app.get('/blog/tags')  # type: flask.Response
        assert response.status_code == 200
        data_str = response.get_data().decode()
        data = json.loads(data_str)
        assert data == {'tags': []}
