from flask import render_template, request
from website.models.account import do_something
from website.models.categories import get_categories

from website.controller.account import bp

@bp.route('/')
def index():
    categories = get_categories()
    return render_template('account/index.html', categories=categories)