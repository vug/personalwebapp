"""
This Blueprint implements Blog related views.
"""
from datetime import datetime
import json

from flask import Blueprint, render_template, abort, request, redirect, jsonify
from flask_misaka import markdown
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
import wtforms

from models import Post, Tag
from extensions import db


blog = Blueprint('blog', __name__)


@blog.route('/')
def blog_index():
    all_posts = Post.query.all()
    all_posts = sorted(all_posts, key=lambda p: p.created_at, reverse=True)
    all_tags = Tag.query.all()
    all_tags = sorted(all_tags, key=lambda t: t.name)
    return render_template('blog_list.html', posts=all_posts, tags=all_tags)


@blog.route('/post/<post_url>')
def blog_post(post_url):
    post = Post.query.filter_by(url=post_url).first()
    if post is None:
        abort(404)
    md_text = post.content
    html = markdown(md_text, fenced_code=True, math=True)
    # https://flask-misaka.readthedocs.io/en/latest/
    # http://misaka.61924.nl/#
    if post.published_at:
        time_str = post.published_at.strftime('%Y-%m-%d %H:%M')
    else:
        time_str = 'not published yet'
    return render_template('blog_post.html', title=post.title, content=html, posted_at=time_str, tags=post.tags)


@blog.route('/tag/<tag_name>')
def blog_tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first()
    return render_template('blog_tag.html', tag=tag, posts=tag.posts)


class BlogEditForm(FlaskForm):
    title = wtforms.StringField('Title', validators=[wtforms.validators.DataRequired()])
    url = wtforms.StringField('Url', validators=[wtforms.validators.DataRequired()])
    content = wtforms.TextAreaField('Content', validators=[wtforms.validators.DataRequired()])
    state = wtforms.SelectField('State', choices=[('1', 'draft'), ('2', 'published')])
    submit = wtforms.SubmitField('Save')


@blog.route('/new')
@login_required
def new_post():
    post = Post(title='Untitled', content='', author_id=current_user.id)
    db.session.add(post)
    db.session.commit()
    return redirect('/blog/edit/{}'.format(post.id))


@blog.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if request.method == 'POST':
        post.url = request.form['url']
        post.title = request.form['title']
        post.content = request.form['content']
        post.edited_at = datetime.utcnow()
        post.state = request.form['state']
        db.session.commit()
        return redirect('/blog/edit/{}'.format(post_id))
    form = BlogEditForm(title=post.title, content=post.content, url=post.url, state=post.state)
    return render_template('blog_edit.html', form=form, post=post)


@blog.route('/preview', methods=['POST'])
def preview_post():
    md_text = request.form['markdown']
    return markdown(md_text, fenced_code=True, math=True)


# TODO: implement delete route
@blog.route('/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    """Delete post with given ID from DB."""
    pass


# Tag API
@blog.route('/tags', methods=['GET', 'POST'])
def tag_index():
    if request.method == 'GET':
        return get_all_tags()

    elif request.method == 'POST':
        name = request.args.get('name')
        if name is None:
            return missing_parameter_error('name')
        return create_tag(name)


@blog.route('/tags/<int:tag_id>', methods=['GET', 'PUT', 'DELETE'])
def tag_id(tag_id):
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
    response = [tag.serialize() for tag in all_tags]
    return jsonify(tags=response), 200


def create_tag(name):
    """Insert a new tag into Tag table.

    :type name: str
    :return: inserted tag in jsonified form
    """
    tag_with_same_name = Tag.query.filter_by(name=name).first()
    if tag_with_same_name:
        return jsonify(error='duplication')
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    response = new_tag.serialize()
    uri = '/blog/tag/{}'.format(new_tag.id)
    return jsonify(tag=response, uri=uri), 201


def get_tag(tag):
    """Return the jsonified form of tag.

    :type tag: Tag
    """
    response = tag.serialize()
    return jsonify(tag=response), 200


def update_tag(new_name, tag):
    """Update the tag in Tag table with given new_name.

    :type new_name: str
    :type tag: Tag
    :return: updated tag in jsonified form
    """
    tag.name = new_name
    db.session.commit()
    response = tag.serialize()
    uri = '/blog/tag/{}'.format(tag.id)
    return jsonify(tag=response, uri=uri), 200


def delete_tag(tag):
    """Delete tag from Tag table.

    :type tag: Tag
    :return: deleted tag in jsonified form
    """
    db.session.delete(tag)
    db.session.commit()
    response = tag.serialize()
    return jsonify(tag=response), 200
