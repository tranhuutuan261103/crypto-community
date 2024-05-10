from flask import render_template, request
from website.models.user import register as registerUser

from website.controller.auth import bp

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try: 
            email = request.form.get('email')
            password = request.form.get('password')
            print(email, password)
            user = registerUser(email, password)
            return str('User created successfully')
        except Exception as e:
            return str(e)
    
    return render_template('auth/register.html')