import os
import random

from flask import Flask, render_template, redirect, url_for
from flask_misaka import Misaka, markdown
from flask_sqlalchemy import SQLAlchemy

static_pages = {'about.html', 'projects.html', 'music.html', 'research.html'}

app = Flask(__name__)
Misaka(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # sqlite://<nohostname>/<path>
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def rnd_clr():
    colors = ['#9ad3de', 'rgb(252,123,52)', '#3fb0ac', '#fae596', '#dbe9d8', '#f2efe8', '#fccdd3']
    return random.choice(colors)


@app.route('/<name>')
def static_page(name):
    if name in static_pages:
        return render_template(name, bg_color=rnd_clr())
    else:
        return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('home.html', bg_color=rnd_clr())


@app.route('/blog/')
def blog():
    post_list = os.listdir('posts')
    return render_template('blog_list.html', post_list=post_list)


@app.route('/blog/<post>')
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
