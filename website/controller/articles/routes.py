from flask import render_template, request
from website.models.articles import do_something

from website.controller.articles import bp

@bp.route('/')
def index():
    do_something()
    return render_template('articles/index.html')