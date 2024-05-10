from flask import Blueprint

bp = Blueprint('auth', __name__)

from website.controller.auth import routes