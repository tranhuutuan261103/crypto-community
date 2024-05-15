from flask import render_template, request, jsonify, session
from flask_uploads import UploadSet, IMAGES
# Khởi tạo Flask-Uploads
photos = UploadSet('photos', IMAGES)
from website.models.categories import get_categories
from website.models.post import get_posts, get_sorted_posts, get_post, like_post, create_post
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import datetime
from website.middlewares.auth import login_required, login_check

from website.controller.posts import bp

@bp.route('/')
@login_check
def index(user_id=None):
    categories = get_categories()
    posts = get_sorted_posts("b9JzFIcDQtXurNFI8wyD", 10, user_id)
    return render_template('post/index.html', posts=posts, categories=categories)

@bp.route('/<string:post_id>')
@login_check
def detail(post_id, user_id=None):
    categories = get_categories()
    post = get_post(post_id, user_id)
    return render_template('post/detail.html', post=post, categories=categories)


@bp.route('/like', methods=['POST'])
@login_required
def like():
    post_id = request.json.get('post_id')  # Correct method to access JSON data
    user_id = session['user']['localId']
    try:
        response = like_post(post_id, user_id)
        return jsonify(response), 200  # Ensure you return a JSON response
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Provide error message in response

@bp.route('/create', methods=['POST'])
@login_required
def create():
    # Lấy dữ liệu post từ request JSON
    post = request.form.to_dict()

    # Tải ảnh lên nếu có
    if 'thumbnail' in request.files:
        thumbnail = request.files['thumbnail']
    else:
        thumbnail = None

    post['liked_by'] = []

    user_id = session['user']['localId']
    name = session['user']['displayName']
    avatar = session['user']['photoUrl'] if 'photoUrl' in session['user'] else ''
    post['posted_by'] ={
        'name': name if name != '' else 'Anonymous',
        'avatar': avatar if avatar != '' else 'https://via.placeholder.com/150',
        'user_id': user_id
    }
    post['created_at'] = datetime.datetime.now()
    post['eye'] = 0

    try:
        response = create_post(post, thumbnail)
        print("response", response)
        return jsonify(response), 200  # Đảm bảo bạn trả về một phản hồi JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@bp.route('/cryptocurrency')
def cryptocurrency():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
        'start':'1',
        'limit':'10',
        'sort':'cmc_rank',
        'listing_status':'active',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '0cc4a324-e9e3-4a7a-89b5-c5ebffbaa8c6',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        result = json.loads(response.text)
        data = result['data']
        return jsonify(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)