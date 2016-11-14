"""
This Blueprint implements Blog related views.
"""
from flask import Blueprint, render_template, abort, request
from flask_misaka import markdown
from flask_login import login_required
from flask_wtf import FlaskForm
import wtforms

from models import Post, Tag


blog = Blueprint('blog', __name__)


@blog.route('/')
def blog_index():
    all_posts = Post.query.all()
    all_posts = sorted(all_posts, key=lambda p: p.published_at, reverse=True)
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
    time_str = post.published_at.strftime('%Y-%m-%d %H:%M')
    return render_template('blog_post.html', title=post.title, content=html, posted_at=time_str, tags=post.tags)


@blog.route('/tag/<tag_name>')
def blog_tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first()
    return render_template('blog_tag.html', tag=tag, posts=tag.posts)


class BlogEditForm(FlaskForm):
    title = wtforms.StringField('Title', validators=[wtforms.validators.DataRequired()])
    content = wtforms.TextAreaField('Content', validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField('Save')


@blog.route('/edit/<post_url>', methods=['GET', 'POST'])
@login_required
def edit_post(post_url):
    if request.method == 'POST':
        form = BlogEditForm(request.form)
        return 'posted<br>request.form["title"]: {}<br>form.title: {}'.format(request.form['title'], form.title)
    post = Post.query.filter_by(url=post_url).first()
    form = BlogEditForm(title=post.title, content=post.content)
    return render_template('blog_edit.html', form=form, post=post)
