from flask import Blueprint

bp = Blueprint('account', __name__)

from website.controller.account import routes