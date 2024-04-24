import sys
sys.path.append('./website')
from website.db_config.firebase import db

post_ref = db.collection('posts')

def create_post(post):
    try:
        return True
    except Exception as e:
        return str(e)
    
def get_posts():
    try:
        all_posts = [doc.to_dict() for doc in post_ref.stream()]
        return all_posts
    except Exception as e:
        return str(e)