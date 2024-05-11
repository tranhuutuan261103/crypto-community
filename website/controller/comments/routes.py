from flask import render_template, request, jsonify
from website.models.comment import get_comments

from website.controller.comments import bp

@bp.route('/', methods=['GET'])
def get_comments_route():
    post_id = request.args.get('post_id')
    comments = get_comments(post_id)
    return jsonify(comments)