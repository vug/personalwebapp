"""
This Blueprint implements Blog related views.
"""
from datetime import datetime, timedelta

from flask import Blueprint, render_template, abort, request, redirect, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField

from models import Post, Tag, PostState
from extensions import db

blog = Blueprint('blog', __name__)


@blog.route('/')
def blog_index():
    """Render list of all posts. If user is logged in also display links for creating new post and editing posts."""
    all_posts = Post.query.all()
    all_posts = sorted(all_posts, key=lambda p: p.created_at, reverse=True)
    all_tags = Tag.query.all()
    all_tags = sorted(all_tags, key=lambda t: t.name)
    return render_template('blog_list.html', posts=all_posts, tags=all_tags)


@blog.route('/post/<post_url>')
def blog_post(post_url):
    """Render post of given url."""
    post = Post.query.filter_by(url=post_url).first()
    if post is None:
        abort(404)
    timezone_diff = timedelta(hours=post.timezone)
    return render_template('blog_post.html', post=post, tz_diff=timezone_diff)


@blog.route('/new')
@login_required
def new_post():
    """Create a new post in database and redirect to editing that post."""
    post = Post(title='Untitled', content='', author_id=current_user.id, timezone=current_user.timezone)
    db.session.add(post)
    db.session.commit()
    return redirect('/blog/edit/{}'.format(post.id))


class BlogEditForm(FlaskForm):
    """WTForm to edit a blog post."""
    title = wtforms.StringField('Title', validators=[wtforms.validators.DataRequired()])
    url = wtforms.StringField('Url', validators=[wtforms.validators.DataRequired()])
    content = wtforms.TextAreaField('Content', validators=[wtforms.validators.DataRequired()])
    state = QuerySelectField('State', query_factory=lambda: db.session.query(PostState))
    tags = QuerySelectMultipleField('Tags', query_factory=lambda: db.session.query(Tag), get_label=lambda tag: tag.name)
    submit = wtforms.SubmitField('Save')


@blog.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """GET shows post's content in a BlogEditForm. Post gets entered information via the Form into post and save."""
    post = Post.query.filter_by(id=post_id).first()
    form = BlogEditForm(request.form, post)
    if request.method == 'POST' and form.validate_on_submit():
        form_state = PostState.query.filter_by(id=int(request.form.get('state'))).first()
        is_published = post.state.name == 'draft' and form_state.name == 'published'
        is_edited = post.state.name == 'published' and form_state.name == 'published'
        is_drafted = post.state.name == 'published' and form_state.name == 'draft'
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


@blog.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete post with given ID from DB."""
    post = Post.query.filter_by(id=post_id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect('/blog')


@blog.route('/preview', methods=['POST'])
def preview_post():
    """View to return rendered marked into html to be used via an async request."""
    markdown_text = request.form.get('markdown', '')
    html = render_template('blog_preview.html', content=markdown_text)
    return html


@blog.route('/tag/<tag_name>')
def blog_tag(tag_name):
    """Render the list of all posts with given tag."""
    tag = Tag.query.filter_by(name=tag_name).first()
    return render_template('blog_tag.html', tag=tag, posts=tag.posts)


@blog.route('/edit_tags')
@login_required
def edit_tags():
    all_tags = Tag.query.order_by(Tag.name).all()
    return render_template('blog_edit_tags.html', tags=all_tags)
