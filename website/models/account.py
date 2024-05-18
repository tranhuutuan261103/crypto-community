from website.db_config.firebase import db, bucket
from google.cloud import firestore
from firebase_admin import auth
import time as Time

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
    
def update_profile(account_id: str, fullname: str, bio: str):
    try:
        user_id = users_ref.where('account_id', '==', account_id).get()[0].id
        user = users_ref.document(user_id)
        user.update({
            'fullname': fullname,
            'bio': bio
        })
        return True
    except Exception as e:
        print(e)
        return False
    
def update_avatar(account_id, avatar):
    try:
        # Upload image to Firebase Storage
        content_type = avatar.content_type

        image_url = f"avatars/{Time.time()}_{avatar.filename}"
        blob = bucket.blob(image_url)
        blob.upload_from_file(avatar, content_type=content_type)
        blob.make_public()

        # Update user's avatar
        user_id = users_ref.where('account_id', '==', account_id).get()[0].id
        user = users_ref.document(user_id)
        user.update({
            'avatar': blob.public_url
        })

        return blob.public_url
    except Exception as e:
        print(e)
        return None
    
def update_background(account_id, background):
    try:
        # Upload image to Firebase Storage
        content_type = background.content_type

        image_url = f"backgrounds/{Time.time()}_{background.filename}"
        blob = bucket.blob(image_url)
        blob.upload_from_file(background, content_type=content_type)
        blob.make_public()

        # Update user's background
        user_id = users_ref.where('account_id', '==', account_id).get()[0].id
        user = users_ref.document(user_id)
        user.update({
            'background': blob.public_url
        })

        return blob.public_url
    except Exception as e:
        print(e)
        return None