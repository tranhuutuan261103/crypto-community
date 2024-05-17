from flask import request, jsonify, session, redirect
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            if request.path == '/account/':
                return redirect('/post')
            return jsonify({'error': 'Login required', 'code': 401})
        return f(*args, **kwargs)
    return decorated_function

def login_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return f(*args, **kwargs, user_id=None)
        # if str(request.authorization)[7:] != session['user']['idToken']:
        #     return f(*args, **kwargs, user_id=None)
        return f(*args, **kwargs, user_id=session['user']['localId'])
    return decorated_function