"""
This Blueprint implements Blog related views.
"""
from flask import Blueprint, render_template, abort
from flask_misaka import markdown

from models import Post, Tag


blog = Blueprint('blog', __name__)


@blog.route('/')
def blog_index():
    all_posts = Post.query.all()
    all_posts = sorted(all_posts, key=lambda p: p.published_at, reverse=True)
    all_tags = Tag.query.all()
    all_tags = sorted(all_tags, key=lambda t: t.name)
    return render_template('blog_list.html', posts=all_posts, tags=all_tags)


@blog.route('/<post_url>')
def blog_post(post_url):
    post = Post.query.filter_by(url=post_url).first()
    if post is None:
        abort(404)
    md_text = post.content
    html = markdown(md_text, fenced_code=True, math=True)
    # https://flask-misaka.readthedocs.io/en/latest/
    # http://misaka.61924.nl/#
    return render_template('blog_post.html', title=post.title, content=html, date=post.published_at, tags=post.tags)
