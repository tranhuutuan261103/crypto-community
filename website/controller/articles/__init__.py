from flask import Blueprint

bp = Blueprint('articles', __name__)

from website.controller.articles import routes