from website.db_config.firebase import db
from google.cloud import firestore

article_ref = db.collection('articles')

def do_something():
    pass