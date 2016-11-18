"""Routes for Tags REST API"""
from flask import Blueprint, request, jsonify, render_template

from extensions import db
from models import Tag

tags_api = Blueprint('tags', __name__)


@tags_api.route('/tags', methods=['GET', 'POST'])
def tags_index():
    if request.method == 'GET':
        return get_all_tags()

    elif request.method == 'POST':
        name = request.args.get('name')
        if name is None:
            return missing_parameter_error('name')
        return create_tag(name)


@tags_api.route('/tags/<int:tag_id>', methods=['GET', 'PUT', 'DELETE'])
def tags_id(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first()
    if tag is None:
        return missing_tag_error(tag_id)

    if request.method == 'GET':
        return get_tag(tag)

    elif request.method == 'PUT':
        new_name = request.args.get('name')
        if new_name is None:
            return missing_parameter_error('name')
        return update_tag(new_name, tag)

    elif request.method == 'DELETE':
        return delete_tag(tag)


def missing_parameter_error(parameter):
    response = {'message': 'Missing required parameter', 'parameter': parameter}
    return jsonify(error=response), 400


def missing_tag_error(tag_id):
    response = {'message': 'Resource not found', 'id': tag_id}
    return jsonify(error=response), 404


def get_all_tags():
    """Get all tags from Tag table in jsonified form."""
    all_tags = Tag.query.all()
    all_tag_dicts = [tag.serialize() for tag in all_tags]
    return jsonify(tags=all_tag_dicts), 200


def create_tag(name):
    """Insert a new tag into Tag table.

    :type name: str
    :return: inserted tag in jsonified form
    """
    tag_with_given_name_exists = Tag.query.filter_by(name=name).first() is not None
    if tag_with_given_name_exists:
        response = {'message': 'Tag exists', 'name': name}
        return jsonify(error=response), 409  # Conflict
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    new_tag_dict = new_tag.serialize()
    uri = '/blog/tag/{}'.format(new_tag.id)
    return jsonify(tag=new_tag_dict, uri=uri), 201


def get_tag(tag):
    """Return the jsonified form of tag.

    :type tag: Tag
    """
    tag_dict = tag.serialize()
    return jsonify(tag=tag_dict), 200


def update_tag(new_name, tag):
    """Update the tag in Tag table with given new_name.

    :type new_name: str
    :type tag: Tag
    :return: updated tag in jsonified form
    """
    tag.name = new_name
    db.session.commit()
    tag_dict = tag.serialize()
    uri = '/blog/tag/{}'.format(tag.id)
    return jsonify(tag=tag_dict, uri=uri), 200


def delete_tag(tag):
    """Delete tag from Tag table.

    :type tag: Tag
    :return: deleted tag in jsonified form
    """
    db.session.delete(tag)
    db.session.commit()
    tag_dict = tag.serialize()
    return jsonify(tag=tag_dict), 200
