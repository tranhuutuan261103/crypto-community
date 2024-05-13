from flask import render_template, request, jsonify
from website.models.comment import get_comments, get_comment_by_id , add_comment, reply_comment, like_comment

from website.controller.comments import bp

@bp.route('/', methods=['GET'])
def get_comments_route():
    post_id = request.args.get('post_id')
    comments = get_comments(post_id)
    return jsonify(comments)

@bp.route('/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = get_comment_by_id(comment_id)
    return jsonify(comment)

@bp.route('/create', methods=['POST'])
def create_comment():
    parent_id = request.json['parent_comment_id'] if 'parent_comment_id' in request.json else None
    post_id = request.json['post_id']
    user_id = "user_id"
    content = request.json['content']
    return jsonify(add_comment(post_id, user_id, parent_id, content))

@bp.route('/<comment_id>/reply', methods=['POST'])
def reply_comment_route(comment_id):
    parent_id = request.json['parent_comment_id']
    comment_reply_user_id = comment_id
    post_id = request.json['post_id']
    user_id = "user_id"
    content = request.json['content']
    return jsonify(reply_comment(post_id, user_id, parent_id, comment_reply_user_id, content))

@bp.route('/<comment_id>/like', methods=['POST'])
def like_comment_route(comment_id):
    return jsonify(like_comment(comment_id, "user_id"))