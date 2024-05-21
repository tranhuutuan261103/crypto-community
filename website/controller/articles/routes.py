from flask import render_template, request, jsonify
from website.models.articles import get_article_by_id, get_article_sorted_by_view, get_article_sorted_by_view_type, get_articles_by_highlight, get_articles_by_type, update_views

from website.controller.articles import bp
from website.models.categories import get_categories

@bp.route('/')
def index():
    categories = get_categories()
    articles = {}
    for category in categories:
        articles[category['title']] = [article for article in get_articles_by_type(category['title'], 3)]
    articles_highlight = get_articles_by_highlight()
    articles_sorted_by_view = get_article_sorted_by_view()
    return render_template('articles/index.html', articles=articles, categories=categories, articles_highlight=articles_highlight, articles_sorted_by_view=articles_sorted_by_view, active='articles')

@bp.route('/category/<string:category_name>')
def category(category_name):
    categories = get_categories()
    articles = []
    articles = get_articles_by_type(category_name)
    articles_sorted_by_view = get_article_sorted_by_view_type(category_name)
    return render_template('articles/category.html', articles=articles, category_name=category_name, categories=categories, articles_sorted_by_view=articles_sorted_by_view, active=category_name)

@bp.route('/<string:article_id>')
def detail(article_id):
    categories = get_categories()
    article = get_article_by_id(article_id)
    return render_template('articles/detail.html', article=article, categories=categories)

@bp.route('/view', methods=['POST'])
def view():
    article_id = request.json.get('article_id')
    try:
        response = update_views(article_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500