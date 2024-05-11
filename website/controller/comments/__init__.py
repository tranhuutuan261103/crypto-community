from flask import Blueprint

bp = Blueprint('comments', __name__)

from website.controller.comments import routes