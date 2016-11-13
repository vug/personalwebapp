"""
This Blueprint collects the static pages such as main index and about, projects etc.
"""
import random

from flask import Blueprint, render_template, abort

static_pages = Blueprint('static_pages', __name__)

pages = {'about.html', 'projects.html', 'music.html', 'research.html'}


def rnd_clr():
    colors = ['#9ad3de', 'rgb(252,123,52)', '#3fb0ac', '#fae596', '#dbe9d8', '#f2efe8', '#fccdd3']
    return random.choice(colors)


@static_pages.route('/<name>')
def static_page(name):
    if name in pages:
        return render_template(name, bg_color=rnd_clr())
    abort(404)


@static_pages.route('/')
def index():
    return render_template('home.html', bg_color=rnd_clr())
