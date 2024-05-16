from flask import render_template, request
from website.models.account import do_something

from website.controller.account import bp

@bp.route('/')
def index():
    do_something()
    return render_template('account/index.html')