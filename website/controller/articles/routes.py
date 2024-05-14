from flask import render_template, request
from website.models.articles import do_something, get_articles_by_type

from website.controller.articles import bp

@bp.route('/')
def index():
    news_articles = get_articles_by_type('news');
    return render_template('articles/index.html', news_articles = news_articles)

@bp.route('/category')
def category():
    do_something()
    return render_template('articles/category.html')

@bp.route('/id')
def detail():
    do_something()
    return render_template('articles/detail.html')