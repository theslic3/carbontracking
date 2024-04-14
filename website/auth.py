from flask import Blueprint, render_template, request, jsonify, Response, redirect, url_for
from website.dashboard.userValidation import *
from email_validator import validate_email, EmailNotValidError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Users
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()
        #if user and user.password == password:
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect('/mainmenu')
        else:
            return render_template('signin.html', error='Invalid email or password')
    return render_template('signin.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if not is_valid_email(email):
            return render_template('register.html', error='Please enter a valid email.')
        if not is_valid_name(name):
            return render_template('register.html', error='Please enter a real name.')
        if not is_valid_password(password1):
            return render_template('register.html', error='Please enter a stronger password') #: 8<Length<20, min 1 upper case, 1 lower case, 1 symbol, 1 number.)')
        if password1 != password2:
            return render_template('register.html', error='Ensure Passwords Match')

        if Users.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already exists')

        # Create a new user
        new_user = Users(email=email, name=name, password=generate_password_hash(password1, method='pbkdf2:sha256'))

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user, remember=True)

        return redirect(url_for('views.show_dashboard'))

    return render_template('register.html')

@auth.route('/reset', methods=['GET'])
def reset():
    return render_template('forgotpassword.html')

@auth.route('/signout', methods=['GET', 'POST'])
@login_required
def signout():
    logout_user()
    return redirect('/signin')
