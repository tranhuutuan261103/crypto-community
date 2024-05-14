from flask import render_template, request
from website.models.admin import do_something

from website.controller.admin import bp

@bp.route('/')
def index():
    do_something()
    return render_template('admin/index.html')