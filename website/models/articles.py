from website.db_config.firebase import db
from google.cloud import firestore

article_ref = db.collection('articles')

def do_something():
    pass

def get_articles_by_type(article_type):
    try:
        all_articles = []
        query = article_ref.where('type', '==', article_type).order_by('created_at', direction="DESCENDING")
        for article in query.stream():
            article_data = article.to_dict()
            article_data['id'] = article.id
            all_articles.append(article_data)
        return all_articles
    except Exception as e:
        return str(e)

def get_articles_by_highlight():
    try:
        all_articles = []
        query = article_ref.where('highlight', '==', True).order_by('created_at', direction="DESCENDING")
        for article in query.stream():
            article_data = article.to_dict()
            article_data['id'] = article.id
            all_articles.append(article_data)
        return all_articles
    except Exception as e:
        return str(e)
    
def get_article_by_id(article_id):
    try:
        article = article_ref.document(article_id).get()
        article_data = article.to_dict()
        article_data['id'] = article_id
        return article_data
    except Exception as e:
        return str(e)

def get_article_sorted_by_view():
    try:
        all_articles = []
        query = article_ref.order_by('views', direction="DESCENDING").limit(10)
        for article in query.stream():
            article_data = article.to_dict()
            article_data['id'] = article.id
            all_articles.append(article_data)
        return all_articles
    except Exception as e:
        return str(e)

def get_article_sorted_by_view_type(article_type):
    try:
        all_articles = []
        query = article_ref.where('type', '==', article_type).order_by('views', direction="DESCENDING").limit(10)
        for article in query.stream():
            article_data = article.to_dict()
            article_data['id'] = article.id
            all_articles.append(article_data)
        return all_articles
    except Exception as e:
        return str(e)
    
def update_views(article_id):
    try:
        article = article_ref.document(article_id)
        article.update({'views': firestore.Increment(1)})
        return True
    except Exception as e:
        return False