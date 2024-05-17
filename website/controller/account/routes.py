from flask import render_template, request, session, jsonify
from website.models.account import get_profile
from website.models.categories import get_categories
from website.middlewares.auth import login_required

from website.controller.account import bp

@bp.route('/')
@login_required
def index():
    account_id = session['user']['localId']
    profile = get_profile(account_id)
    categories = get_categories()
    return render_template('account/index.html', categories=categories, profile=profile)

@bp.route('/info')
@login_required
def info():
    account_id = session['user']['localId']
    profile = get_profile(account_id)
    return jsonify({
        'status': '200',
        'profile': profile
    })