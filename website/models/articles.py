from website.db_config.firebase import db
from google.cloud import firestore

article_ref = db.collection('articles')

def do_something():
    pass

def get_articles_by_type(type):
    try:
        all_articles = []
        for article in article_ref.where('type', '==', type).order_by('date', direction=firestore.Query.DESCENDING).stream():
            article_data = article.to_dict()
            article_data['id'] = article.id
            all_articles.append(article_data)
        return all_articles
    except Exception as e:
        return str(e)