from flask import Blueprint

bp = Blueprint('post', __name__)

from website.controller.posts import routes