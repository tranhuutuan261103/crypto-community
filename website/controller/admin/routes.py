from flask import redirect, render_template, request, jsonify, session, url_for
from website.controller.admin.crawl_article import ArticleCrawler
from website.models.admin import do_something

from website.controller.admin import bp
from website.models.articles import check_article_exist, create_post, get_article_by_id, get_articles, get_information_index, get_num_articles, get_num_articles_by_type, get_num_views, update_highlight_article, update_status_article
from website.models.categories import get_all_categories, get_categories, get_num_categories, update_status_category
from website.models.user import get_num_admins, get_num_users
from website.models.user import register as registerUser, login as loginUser, get_user

@bp.route('/')
def index():
    num_articles = 0;
    num_views = 0;
    num_categories = 0;
    num_users = get_num_users()
    num_admins = get_num_admins()
    categories = get_categories()
    num_articles_by_category = {}
    num_articles, num_views,num_articles_by_category = get_information_index(categories)
    num_categories = len(categories)
    user = session.get('user')
    return render_template('admin/index.html', num_articles=num_articles, num_views=num_views, num_categories=num_categories, categories=categories, num_users=num_users, num_admins=num_admins, num_articles_by_category=num_articles_by_category, active='index', user=user)

@bp.route('/category')
def category():
    categories = get_all_categories()
    user = session.get('user')
    return render_template('admin/categories.html', categories=categories, active='category', user=user)

@bp.route('/category/status', methods=['POST'])
def update_category_status():
    category_id = request.json.get('category_id')
    status = request.json.get('status')
    try:
        response = update_status_category(category_id, status)
        return jsonify({'status': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@bp.route('/article')
def article():
    articles = get_articles()
    categories = get_all_categories()
    user = session.get('user')
    return render_template('admin/articles.html', articles=articles, categories=categories, active='article', user=user)

@bp.route('/<string:article_id>')
def detail(article_id):
    article = get_article_by_id(article_id)
    user = session.get('user')
    return render_template('admin/detail.html', article=article, user=user)

@bp.route('/article/status', methods=['POST'])
def update_article_status():
    article_id = request.json.get('article_id')
    status = request.json.get('status')
    try:
        response = update_status_article(article_id, status)
        return jsonify({'status': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@bp.route('/article/highlight', methods=['POST'])
def update_article_highlight():
    article_id = request.json.get('article_id')
    status = request.json.get('status')
    try:
        response = update_highlight_article(article_id, status)
        return jsonify({'status': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@bp.route('/crawl', methods=['POST'])
def crawl():
    url = request.json.get('url')
    type = request.json.get('type')
    try:
        crawler = ArticleCrawler('C:/chromedriver-win64/chromedriver.exe')
        response = crawler.crawl_article(url, type)
        unique_articles = check_article_exist(response)
        for article in unique_articles:
            create_post(article)
        if response is None:
            raise Exception("Không thu thập được bài viết")
        return jsonify({'num_article': len(response), 'num_unique' : len(unique_articles)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try: 
            username = request.form.get('username')
            password = request.form.get('password')
            user = loginUser(username, password)
            if user['role'] == 'admin':
                session['user'] = user
                return redirect(url_for('admin.index'))  # Redirect to the index page for admin
            else:
                raise Exception('User is not admin')
        except Exception as e:
            return render_template('admin/login.html', error=str(e))
        
    return render_template('admin/login.html')

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    print(session)
    return redirect(url_for('admin.login'))