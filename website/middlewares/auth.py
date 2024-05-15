from flask import request, jsonify, session
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Login required', 'code': 401})
        if str(request.authorization)[7:] != session['user']['idToken']:
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