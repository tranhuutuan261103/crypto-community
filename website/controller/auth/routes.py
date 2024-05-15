from flask import render_template, request, jsonify, session
from website.models.user import register as registerUser, login as loginUser, get_user

from website.controller.auth import bp

@bp.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try: 
            email = request.form.get('email')
            password = request.form.get('password')
            name = "Some Name"
            user = registerUser(email, password, name)
            # Add user to session
            session['user'] = user
            return jsonify({
                'message': 'User registered successfully',
                'token': user.get('idToken'),
                'email': user.get('email'),
                'user_name': user.get('displayName'),
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
            return jsonify({
                'message': 'User logged in successfully',
                'token': user.get('idToken'),
                'email': user.get('email'),
                'user_name': user.get('displayName'),
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