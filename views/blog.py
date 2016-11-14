"""
This Blueprint implements Blog related views.
"""
from datetime import datetime

from flask import Blueprint, render_template, abort, request, redirect
from flask_misaka import markdown
from flask_login import login_required, current_user
from flask_wtf import Form
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


class BlogEditForm(Form):
    title = wtforms.StringField('Title', validators=[wtforms.validators.DataRequired()])
    url = wtforms.StringField('Url', validators=[wtforms.validators.DataRequired()])
    content = wtforms.TextAreaField('Content', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Save')


@blog.route('/new')
@login_required
def new_post():
    post = Post(title='Untitled', content='', author_id=current_user.id)
    post.url = make_url_unique(post.url)
    db.session.add(post)
    db.session.commit()
    return redirect('/blog/edit/{}'.format(post.id))


@blog.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if request.method == 'POST':
        post.url = make_url_unique(request.form['url'])
        post.title = request.form['title']
        post.content = request.form['content']
        post.edited_at = datetime.utcnow()
        db.session.commit()
        return redirect('/blog/edit/{}'.format(post_id))
    form = BlogEditForm(title=post.title, content=post.content, url=post.url)
    return render_template('blog_edit.html', form=form, post=post)


def make_url_unique(url):
    """Append "_" to URL until no matches are in Post table."""
    while True:
        is_unique = Post.query.filter_by(url=url).count() < 2
        if is_unique:
            break
        url += '_'
    return url
