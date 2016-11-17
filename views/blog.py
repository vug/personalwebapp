"""
This Blueprint implements Blog related views.
"""
from datetime import datetime

from flask import Blueprint, render_template, abort, request, redirect, jsonify, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

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
    return render_template('blog_post.html', post=post)


@blog.route('/tag/<tag_name>')
def blog_tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first()
    return render_template('blog_tag.html', tag=tag, posts=tag.posts)


class BlogEditForm(FlaskForm):
    title = wtforms.StringField('Title', validators=[wtforms.validators.DataRequired()])
    url = wtforms.StringField('Url', validators=[wtforms.validators.DataRequired()])
    content = wtforms.TextAreaField('Content', validators=[wtforms.validators.DataRequired()])
    state = wtforms.SelectField('State', choices=[('1', 'draft'), ('2', 'published')])
    tags = QuerySelectMultipleField('Tags', query_factory=lambda: db.session.query(Tag), get_label=lambda tag: tag.name)
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
    form = BlogEditForm(request.form, post)
    if request.method == 'POST' and form.validate_on_submit():
        is_published = post.state == 1 and request.form.get('state', '3') == '2'
        is_edited = post.state == 2 and request.form.get('state', '3') == '2'
        is_drafted = post.state == 2 and request.form.get('state', '3') == '1'
        if is_published:
            post.published_at = datetime.utcnow()
        elif is_edited:
            post.edited_at = datetime.utcnow()
        elif is_drafted:
            post.published_at = None
            post.edited_at = None
        form.populate_obj(post)
        db.session.commit()
        flash('(Post saved)')
        return redirect('/blog/edit/{}'.format(post_id))
    return render_template('blog_edit.html', form=form, post=post)


@blog.route('/preview', methods=['POST'])
def preview_post():
    markdown_text = request.form.get('markdown', '')
    html = Post.render_markdown(markdown_text)
    return html


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


@blog.route('/edit_tags')
def edit_tags():
    all_tags = Tag.query.order_by(Tag.name).all()
    return render_template('blog_edit_tags.html', tags=all_tags)
