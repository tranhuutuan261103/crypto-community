from flask import render_template, request, jsonify, session
from website.models.comment import get_comments, get_comment_by_id , add_comment, reply_comment, like_comment
from website.middlewares.auth import login_required, login_check

from website.controller.comments import bp

@bp.route('/', methods=['GET'])
@login_check
def get_comments_route(user_id=None):
    post_id = request.args.get('post_id')
    comments = get_comments(post_id, user_id)
    return jsonify(comments)

@bp.route('/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = get_comment_by_id(comment_id)
    return jsonify(comment)

@bp.route('/create', methods=['POST'])
@login_required
def create_comment():
    parent_id = request.json['parent_comment_id'] if 'parent_comment_id' in request.json else None
    post_id = request.json['post_id']
    user_id = session['user']['user_id']
    content = request.json['content']
    return jsonify(add_comment(post_id, user_id, parent_id, content))

@bp.route('/<comment_id>/reply', methods=['POST'])
@login_required
def reply_comment_route(comment_id):
    parent_id = request.json['parent_comment_id'] if 'parent_comment_id' in request.json else None
    post_id = request.json['post_id']
    user_id = session['user']['user_id']
    content = request.json['content']
    return jsonify(reply_comment(post_id, user_id, comment_id, parent_id, content))

@bp.route('/<comment_id>/like', methods=['POST'])
@login_required
def like_comment_route(comment_id):
    return jsonify(like_comment(comment_id, session['user']['localId']))