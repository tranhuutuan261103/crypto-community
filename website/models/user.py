from firebase_admin import auth
from website.db_config.firebase_client import auth as authClient

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