from dashboard.calculation import *
import json
from flask import Flask, render_template, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('signin.html')

@app.route('/register',  methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect('/mainMenu')  # Redirect to login page after successful registration

    else:
        return render_template('register.html')

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

if __name__ == '__main__':
    app.run(debug=True)
