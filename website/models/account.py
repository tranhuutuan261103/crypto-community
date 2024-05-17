from website.db_config.firebase import db
from google.cloud import firestore
from firebase_admin import auth

users_ref = db.collection('users')

def get_profile(account_id: str):
    try:
        user = users_ref.where('account_id', '==', account_id).get()[0].to_dict()
        account = auth.get_user(user['account_id'])
        user['email'] = account.email
        return user
    except Exception as e:
        return str(e)
    
def create_profile(account_id: str, email: str, fullname: str, avatar: str = None):
    try:
        users_ref.add({
            'account_id': account_id,
            'fullname': fullname,
            'avatar': avatar,
            'background': None,
            'bio': '',
            'role': 'user',
        })
        return True
    except Exception as e:
        return e