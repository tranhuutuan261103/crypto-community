from flask import render_template, request, jsonify, session
from website.models.user import register as registerUser, login as loginUser, get_user
from website.models.account import get_profile, create_profile

from website.controller.auth import bp

@bp.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try: 
            email = request.form.get('email')
            password = request.form.get('password')
            fullname = request.form.get('fullname')
            user = registerUser(email, password, fullname)
            # Add user to session
            session['user'] = user

            # Create user profile
            create_profile(user.get('localId'), email, fullname)
            user_info = get_profile(user.get('localId'))
            return jsonify({
                'message': 'User registered successfully',
                'email': user_info['email'],
                'fullname': user_info['fullname'],
                'avatar': user_info['avatar'],
                'status': '200'
            })
        except Exception as e:
            return jsonify({
                'error': str(e),
                'message': 'User not registered',
                'status': '404'
            })
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try: 
            email = request.form.get('email')
            password = request.form.get('password')
            user = loginUser(email, password)
            # Add user to session
            session['user'] = user
            user_info = get_profile(user.get('localId'))
            return jsonify({
                'message': 'User logged in successfully',
                'email': user_info['email'],
                'fullname': user_info['fullname'],
                'avatar': user_info['avatar'],
                'status': '200'
            })
        except Exception as e:
            return jsonify({
                'error': str(e),
                'message': 'User not found',
                'status': '404'
            })
        
    return render_template('auth/login.html')

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    print(session)
    return jsonify({
        'message': 'User logged out',
        'status': '200'
    })

@bp.route('/info', methods=['GET', 'POST'])
def info():
    return get_user(request.args.get('id_token'))