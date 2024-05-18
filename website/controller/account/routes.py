from flask import render_template, request, session, jsonify
from website.models.account import get_profile, update_profile, update_avatar, update_background
from website.models.categories import get_categories
from website.models.post import get_sorted_posts
from website.middlewares.auth import login_required

from website.controller.account import bp

@bp.route('/')
@login_required
def index():
    account_id = session['user']['localId']
    profile = get_profile(account_id)
    categories = get_categories()
    my_posts = get_sorted_posts("b9JzFIcDQtXurNFI8wyD", 10, session['user']['user_id'], session['user']['user_id'])
    return render_template('account/index.html', categories=categories, profile=profile, posts=my_posts, active='feed')

@bp.route('/info')
@login_required
def info():
    account_id = session['user']['localId']
    profile = get_profile(account_id)
    return jsonify({
        'status': '200',
        'profile': profile
    })

@bp.route('/detail')
@login_required
def detail():
    categories = get_categories()
    account_id = session['user']['localId']
    profile = get_profile(account_id)
    return render_template('account/detail.html', categories=categories, active='feed', profile=profile)

@bp.route('/update', methods=['POST'])
@login_required
def update():
    account_id = session['user']['localId']
    full_name = request.form['fullname']
    bio = request.form['bio']
    result = update_profile(account_id, full_name, bio)
    if result:
        profile = get_profile(account_id)
        return jsonify({
            'status': '200',
            'profile': profile
        })
    return jsonify({
        'status': '400',
        'message': 'Update failed'
    })
    
@bp.route('/update-avatar', methods=['POST'])
@login_required
def update_avatar_route():
    account_id = session['user']['localId']
    if 'avatar' not in request.files:
        return jsonify({
            'status': '400',
            'message': 'No file part'
        })
    avatar = request.files['avatar']
    result = update_avatar(account_id, avatar=avatar)
    if result:
        profile = get_profile(account_id)
        return jsonify({
            'status': '200',
            'profile': profile
        })
    return jsonify({
        'status': '400',
        'message': 'Update failed'
    })

@bp.route('/update-background', methods=['POST'])
@login_required
def update_background_route():
    account_id = session['user']['localId']
    if 'background' not in request.files:
        return jsonify({
            'status': '400',
            'message': 'No file part'
        })
    background = request.files['background']
    result = update_background(account_id, background=background)
    if result:
        profile = get_profile(account_id)
        return jsonify({
            'status': '200',
            'profile': profile
        })
    return jsonify({
        'status': '400',
        'message': 'Update failed'
    })