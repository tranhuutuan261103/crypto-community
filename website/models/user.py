from firebase_admin import auth
from website.db_config.firebase import db
from website.db_config.firebase_client import auth as authClient

users_ref = db.collection('users')

def register(email, password, name):
    try:
        auth.create_user(
            email=email,
            password=password,
            display_name=name
        )
        user = authClient.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        return str(e)
    
def login(email, password):
    try:
        user = authClient.sign_in_with_email_and_password(email, password)
        user['user_id'] = users_ref.where('account_id', '==', user['localId']).get()[0].id
        user['role'] = users_ref.where('account_id', '==', user['localId']).get()[0].to_dict()['role']
        return user
    except Exception as e:
        print(e)
        return str(e)
    
def get_user(id_token):
    try:
        user = authClient.get_account_info(id_token)
        return user
    except Exception as e:
        return str(e)
    
def get_num_users():
    try:
        all_users = []
        query = users_ref.where('role', '==', 'user')
        for user in query.stream():
            all_users.append(user)
        return len(all_users)
    except Exception as e:
        return str(e)
    
def get_num_admins():
    try:
        all_admins = []
        query = users_ref.where('role', '==', 'admin')
        for user in query.stream():
            all_admins.append(user)
        return len(all_admins)
    except Exception as e:
        return str(e)