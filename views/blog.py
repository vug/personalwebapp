"""
This Blueprint implements Blog related views.
"""
import os

from flask import Blueprint, render_template
from flask_misaka import markdown

blog = Blueprint('blog', __name__)


@blog.route('/')
def blog_index():
    post_list = os.listdir('posts')
    return render_template('blog_list.html', post_list=post_list)


@blog.route('/<post>')
def blog_post(post):
    with open(os.path.join('posts', post), 'rt') as f:
        md_text = f.read()
    html = markdown(md_text, fenced_code=True, math=True)
    first_three_lines = md_text.split('\n')[:3]
    title, date, tags = [line.split('(')[1][:-1] for line in first_three_lines]
    tags = tags.split(',')
    # https://flask-misaka.readthedocs.io/en/latest/
    # http://misaka.61924.nl/#
    return render_template('blog_post.html', post=html, date=date, tags=tags)
