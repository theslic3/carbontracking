from datetime import datetime, date, timedelta
from .models import Users, Test, Footprint
from . import db
from flask import Blueprint, render_template, request, jsonify, Response, redirect, flash, url_for, session
from flask_login import login_required, current_user
from website.dashboard.calculation import *
from website.dashboard.footprintValidation import *
import json

views = Blueprint('views', __name__)

@views.route('/mainmenu', methods=['GET', 'POST'])
@login_required
def show_dashboard():
    return render_template('mainmenu.html') #,user=current_user

@views.route('/lifestyle', methods=['GET', 'POST'])
@login_required
def inputs():
    return render_template('lifestyle.html')

@views.route('/retrieveCalculation', methods= ['POST'])
def emissionFactors():
    response = request.form
    footprint_profile = calculate_carbon_footprint(response, conversion_factors)
    data = {}
    for factor in footprint_profile:
        data[factor] = footprint_profile[factor]

    new_footprint = Footprint(
            user_id=current_user.id,
            date=datetime.now().date(),  # or use the actual date if available
            electricity_emission_factor=footprint_profile['electricity_emission_factor'],
            heating_emission_factor=footprint_profile['heating_emission_factor'],
            car_emission_factor=footprint_profile['car_emission_factor'],
            flight_emission_factor=footprint_profile['flight_emission_factor'],
            meat_and_dairy_emission_factor=footprint_profile['meat_and_dairy_emission_factor'],
            grocery_emission_factor=footprint_profile['grocery_emission_factor'],
            goods_emission_factor=footprint_profile['goods_emission_factor'],
            services_emission_factor=footprint_profile['services_emission_factor'],
            waste_emission_factor=footprint_profile['waste_emission_factor'],
            water_emission_factor=footprint_profile['water_emission_factor'],
            household_size=footprint_profile['household_size'],
            income_category=footprint_profile['income_category'],
            recycling_status=footprint_profile['recycling_status'],
            total_carbon_footprint=footprint_profile['total_carbon_footprint'],
            forecasted_annual_footprint=footprint_profile['forecasted_annual_footprint'],
            regional_annual_average_per_person=footprint_profile['regional_annual_average_per_person'],
            UK_annual_average_per_person=footprint_profile['UK_annual_average_per_person']
        )
    # Check if the user has any previous footprints
    previous_footprint = Footprint.query.filter_by(user_id=current_user.id).order_by(Footprint.date.desc()).first()
    if previous_footprint:
        current_date = datetime.now()
        previous_footprint_date = datetime.combine(previous_footprint.date, datetime.min.time())
        if validation(current_date, previous_footprint_date):
            db.session.add(new_footprint)
            db.session.commit()
            return render_template('mainmenu.html', message="New Monthly Footprint Succesfully calculated. Visit breakdown to see your results! ")
        else:
            session['potential_footprint'] = data
            return redirect('/potential_overwrite')
    # If no previous footprint,  add the new footprint to the database
    db.session.add(new_footprint)
    db.session.commit()
    return render_template('mainmenu.html', message="You've submitted your first emissions data! ")


@views.route('/potential_overwrite', methods=['GET'])
def potential_overwrite():
    return render_template('lifestyle.html', warning='Potential Overwrite')

@views.route('/overwrite', methods=['GET'])
def overwrite():
    footprint_profile = session.get('potential_footprint')
    response = request.args.get('response')
    new_footprint = Footprint(
        user_id=current_user.id,
        date=datetime.now().date(),  # or use the actual date if available
        electricity_emission_factor=footprint_profile['electricity_emission_factor'],
        heating_emission_factor=footprint_profile['heating_emission_factor'],
        car_emission_factor=footprint_profile['car_emission_factor'],
        flight_emission_factor=footprint_profile['flight_emission_factor'],
        meat_and_dairy_emission_factor=footprint_profile['meat_and_dairy_emission_factor'],
        grocery_emission_factor=footprint_profile['grocery_emission_factor'],
        goods_emission_factor=footprint_profile['goods_emission_factor'],
        services_emission_factor=footprint_profile['services_emission_factor'],
        waste_emission_factor=footprint_profile['waste_emission_factor'],
        water_emission_factor=footprint_profile['water_emission_factor'],
        household_size=footprint_profile['household_size'],
        income_category=footprint_profile['income_category'],
        recycling_status=footprint_profile['recycling_status'],
        total_carbon_footprint=footprint_profile['total_carbon_footprint'],
        forecasted_annual_footprint=footprint_profile['forecasted_annual_footprint'],
        regional_annual_average_per_person=footprint_profile['regional_annual_average_per_person'],
        UK_annual_average_per_person=footprint_profile['UK_annual_average_per_person']
    )
    if response == 'yes':
        previous_footprint = Footprint.query.filter_by(user_id=current_user.id).order_by(Footprint.date.desc()).first()
        db.session.delete(previous_footprint)
        db.session.add(new_footprint)
        db.session.commit()
        return render_template('mainmenu.html', message="New Monthly Footprint Succesfully calculated. Visit breakdown to see your results! ")  # Redirect to main menu after overwriting
    elif response == 'no':
        return render_template('mainmenu.html', message="No changes")  # Redirect to main menu without overwriting
    else:
        return redirect('/mainmenu')

@views.route('/testingdates', methods=['GET', 'POST'])
def datetest():
    #previous_footprint = Footprint.query.filter_by(user_id=current_user.id).order_by(Footprint.date.desc()).first()
    new_footprint = Footprint.query.filter_by(user_id=current_user.id, id=9).first()
    if new_footprint:
        current_date = datetime.now()
        new_date = current_date - timedelta(days=30)  # Assuming a month is 30 days
        new_footprint.date = new_date
        db.session.commit()
        #new_footprint = Footprint.query.filter_by(user_id=current_user.id).order_by(Footprint.date.desc()).offset(1).limit(1).first()
        #new_footprint = Footprint.query.filter_by(user_id=current_user.id).order_by(Footprint.date.desc()).first()
        new_footprint = Footprint.query.filter_by(user_id=current_user.id, id=9).first()


        new_footprint_date = str(new_footprint.date)
        return render_template('mainmenu.html', message=new_footprint_date)

@views.route('/retrieve_emissionfactors', methods=['GET', 'POST'])
@login_required
def retrieve():
    most_recent_footprint = get_most_recent_footprint(current_user.id)
    emission_factors_recent = get_footprint_emission_factors(most_recent_footprint)
    electricity = emission_factors_recent['electricity_emission_factor']

    footprints_with_dates = get_previous_footprints_with_dates(current_user.id)

    graph_data = get_graph_data(emission_factors_recent,footprints_with_dates)

    for list in graph_data:
        print(list)

    return render_template('mainmenu.html', message= "Success")


'''
@views.route('/calculation_old', methods=['POST'])
def datetest():
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
'''
