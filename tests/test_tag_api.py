import json

import flask

from .base import TestBase
from extensions import db
from models import Tag


class TestTagApi(TestBase):
    def test_getting_all_tags_when_there_are_no_tags(self):
        response = self.app.get('/blog/tags')  # type: flask.Response
        assert response.status_code == 200
        data_str = response.get_data().decode()
        data = json.loads(data_str)
        assert data == {'tags': []}

    def test_creating_tag(self):
        response = self.app.post('/blog/tags?name=testtag')  # type: flask.Response
        assert response.status_code == 201
        data_str = response.get_data().decode()
        data = json.loads(data_str)
        assert data == {'tag': {'name': 'testtag', 'id': 1}, 'uri': '/blog/tag/1'}
        with self.get_context():
            tag = Tag.query.filter_by(name='testtag').one()
            assert tag is not None
            assert tag.name == 'testtag'

    def test_missing_parameter_when_creating_tag(self):
        response = self.app.post('/blog/tags?tag=testtag')  # type: flask.Response
        assert response.status_code == 400
        data_str = response.get_data().decode()
        data = json.loads(data_str)
        assert data == {'error': {'message': 'Missing required parameter', 'parameter': 'name'}}

    def test_getting_tag_by_id(self):
        self.app.post('/blog/tags?name=testtag')
        response = self.app.get('/blog/tags/1')  # type: flask.Response
        assert response.status_code == 200
        data_str = response.get_data().decode()
        data = json.loads(data_str)
        assert data == {'tag': {'name': 'testtag', 'id': 1}}

    def test_missing_tags_when_getting_tag_by_id(self):
        response = self.app.get('/blog/tags/1')  # type: flask.Response
        assert response.status_code == 404
        data_str = response.get_data().decode()
        data = json.loads(data_str)
        assert data == {'error': {'message': 'Resource not found', 'id': 1}}

