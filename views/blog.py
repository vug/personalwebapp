"""
This Blueprint implements Blog related views.
"""
from flask import Blueprint, render_template, abort
from flask_misaka import markdown

from models import Post


blog = Blueprint('blog', __name__)


@blog.route('/')
def blog_index():
    all_posts = Post.query.all()
    return render_template('blog_list.html', posts=all_posts)


@blog.route('/<post_url>')
def blog_post(post_url):
    post = Post.query.filter_by(url=post_url).first()
    if post is None:
        abort(404)
    md_text = post.content
    html = markdown(md_text, fenced_code=True, math=True)
    first_three_lines = md_text.split('\n')[:3]
    title, date, tags = [line.split('(')[1][:-1] for line in first_three_lines]
    tags = tags.split(',')
    # https://flask-misaka.readthedocs.io/en/latest/
    # http://misaka.61924.nl/#
    return render_template('blog_post.html', post=html, date=date, tags=tags)
