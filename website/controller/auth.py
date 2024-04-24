import sys
sys.path.append('./website')
from website.models.userAPI import register as registerUser
from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
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