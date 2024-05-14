from flask import Blueprint

bp = Blueprint('admin', __name__)

from website.controller.admin import routes