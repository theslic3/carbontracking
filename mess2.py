from dashboard.calculation import *
import json
from flask import Flask, render_template, request, jsonify, Response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite'  # SQLite URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications
db = SQLAlchemy(app)

# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Create database tables
db.create_all()

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        print(request)
        return redirect('/signin.html')
    return render_template('signin.html')

@app.route('/signin', methods=['GET','POST'])
def signin():
    email = request.form['email']
    password = request.form['password']

    # Check if the user exists
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        return redirect('/mainmenu.html')
    else:
        return render_template('signin.html', error='Invalid email or password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already exists')

        # Create a new user
        new_user = User(email=email, name=name, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/signin')  # Redirect to login page after successful registration

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
