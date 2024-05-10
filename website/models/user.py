from firebase_admin import auth

def register(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return user
    except Exception as e:
        return str(e)
    
def get_user(uid):
    try:
        user = auth.get_user(uid)
        return user
    except Exception as e:
        return str(e)