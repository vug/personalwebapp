import json

import flask

from .base import TestBase
from extensions import db
from models import Tag


class TestTagApi(TestBase):
    def test_getting_all_tags_when_there_are_no_tags(self):
        response = self.app.get('/blog/tags')  # type: flask.Response
        code, data = get_status_code_and_data(response)
        assert code == 200
        assert data == {'tags': []}

    def test_creating_tag(self):
        response = self.app.post('/blog/tags?name=testtag')  # type: flask.Response
        code, data = get_status_code_and_data(response)
        assert code == 201
        assert data == {'tag': {'name': 'testtag', 'id': 1}, 'uri': '/blog/tag/1'}
        with self.get_context():
            tag = Tag.query.filter_by(name='testtag').one()
            assert tag is not None
            assert tag.name == 'testtag'

    def test_missing_parameter_when_creating_tag(self):
        response = self.app.post('/blog/tags?tag=testtag')  # type: flask.Response
        code, data = get_status_code_and_data(response)
        assert code == 400
        assert data == {'error': {'message': 'Missing required parameter', 'parameter': 'name'}}

    def test_getting_tag_by_id(self):
        self.app.post('/blog/tags?name=testtag')
        response = self.app.get('/blog/tags/1')  # type: flask.Response
        code, data = get_status_code_and_data(response)
        assert code == 200
        assert data == {'tag': {'name': 'testtag', 'id': 1}}

    def test_missing_tags_when_getting_tag_by_id(self):
        response = self.app.get('/blog/tags/1')  # type: flask.Response
        code, data = get_status_code_and_data(response)
        assert code == 404
        assert data == {'error': {'message': 'Resource not found', 'id': 1}}

    def test_updating_tag(self):
        self.app.post('/blog/tags?name=testtag')
        response = self.app.put('/blog/tags/1?name=updatedtag')  # type: flask.Response
        code, data = get_status_code_and_data(response)
        assert code == 200
        assert data == {'tag': {'name': 'updatedtag', 'id': 1}, 'uri': '/blog/tag/1'}

        response = self.app.get('/blog/tags/1')  # type: flask.Response
        code, data = get_status_code_and_data(response)
        assert code == 200
        assert data == {'tag': {'name': 'updatedtag', 'id': 1}}

        # print(response.status_code, data)
        # print(response.status_code, response.data)


def get_status_code_and_data(response):
    code = response.status_code
    data_str = response.get_data().decode()
    data = json.loads(data_str)
    return code, data
