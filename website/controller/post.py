import sys
sys.path.append('./website')
from website.models.postAPI import get_posts
from flask import Blueprint, render_template, request

post = Blueprint('post', __name__)

@post.route('/')
def index():
    posts = get_posts()
    print(posts)
    return render_template('post/index.html', posts=posts)