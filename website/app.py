from dashboard.calculation import *
from dashboard.userValidation import *
import json
from flask import Flask, render_template, request, jsonify, Response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from email_validator import validate_email, EmailNotValidError

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
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def hello():
    '''
    if request.method == 'POST':
        print(request)
        return redirect('/signin.html')
        '''
    return render_template('mainmenu.html')

@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            return redirect('/mainmenu')
        else:
            return render_template('signin.html', error='Invalid email or password')
    return render_template('signin.html')

@app.route('/register', methods=['GET', 'POST'])
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

        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already exists')

        # Create a new user
        new_user = User(email=email, name=name, password=password1)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/signin')  # Redirect to login page after successful registration

    return render_template('register.html')

@app.route('/mainmenu', methods=['GET', 'POST'])
def show_dashboard():
    return render_template('mainmenu.html')

@app.route('/calculatefootprint', methods=['GET'])
def show_calculate_page():
    print('template retrieved')
    return render_template('calculatefootprint.html')

@app.route('/calculatefootprint', methods=['POST'])
def calculate():
    data = request.form
    electricity = float(data.get('electricity-factor'))
    gas = float(data.get('gas-factor'))
    oil = float(data.get('oil-factor'))
    car_mileage = float(data.get('carmileage-factor'))
    longhaul = float(data.get('longhaul-factor'))
    shorthaul = float(data.get('shorthaul-factor'))
    newspaper = convertRecycling(str(data.get('newspaper-factor')))
    tin = convertRecycling(str(data.get('tin-factor')))

    print(tin, newspaper)

    # Calculate footprint result = calculateFootprint(electricity, gas, oil, car_mileage, longhaul, shorthaul, newspaper, tin
    footprint = calculateFootprint(electricity, gas, oil, car_mileage, longhaul, shorthaul, newspaper, tin)
    message = "Ideal carbon footprint (low) is from 10,000 to 15,999 pounds per year. 16,000-22,000 is considered average."
    proceed = "If you have missed any boxes, these have been defaulted to 0. If you are happy with your submission, click track to save your footprint so we can analyse. If not, please re-enter values for calculation."
    category = categoriseFootprint(footprint)

    response_data = {
    'footprint': footprint,
    'category': category,
    'message': message,
    'trackPrompt': proceed
    }

    reply = json.dumps(response_data)

    response = Response(response=reply, status=200, mimetype='application/json')
    response.headers["Content-Type"]="application/json"
    response.headers["Access-Control-Allow-Origin"]="*"

    return response

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    return redirect('/signin')

if __name__ == '__main__':
    app.run(debug=True)
