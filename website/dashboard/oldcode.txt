from datetime import datetime, timedelta
from models import Footprint


def validate_footprint_date(current_date, footprint_date):
    # Calculate the difference between the current date and the footprint date
    time_difference = current_date - footprint_date

    days_difference = time_difference.days()

    # Ensure that the difference is at least 30 days (1 month)
    if days_difference >= 30:
        return True
    else:
        return False

from datetime import datetime, timedelta

@views.route('/retrieveCalculation', methods=['POST'])
def emissionFactors():
    response = request.form
    footprint_profile = calculate_carbon_footprint(response, conversion_factors)

    # Check if the user has any previous footprints
    previous_footprint = Footprint.query.filter_by(user_id=current_user.id).order_by(Footprint.date.desc()).first()
    if previous_footprint:
        # Get the current date
        current_date = datetime.now()

        # Calculate the difference between the current date and the date of the previous footprint
        time_difference = current_date - previous_footprint.date
        days_difference = time_difference.days

        # If the previous footprint is at least 1 month old, add the new footprint to the database
        if days_difference >= 30:
            add_new_footprint(footprint_profile)
            return redirect('/lifestyle')
        else:
            # Flash a message indicating that the previous footprint will be overwritten if a new one is submitted
            flash('Your previous footprint will be overwritten if you submit a new one. Do you want to proceed?', category='warning')
            return render_template('confirmation.html')  # Assuming you have a confirmation template

    # If there is no previous footprint, simply add the new footprint to the database
    add_new_footprint(footprint_profile)
    return redirect('/lifestyle')


@views.route('/retrieveCalculation', methods= ['POST'])
def emissionFactors():
    response = request.form
    footprint_profile = calculate_carbon_footprint(response, conversion_factors)

    # Create a new Footprint instance with data from the footprint_profile dictionary
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

    # Add the new Footprint instance to the database session
    db.session.add(new_footprint)

    # Commit the changes to the database
    db.session.commit()

    # Redirect to the desired page after adding the footprint
    return redirect('/lifestyle')


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

    @views.route('/testingdates', methods=['GET', 'POST'])
    def datetest():
        #previous_footprint = Footprint.query.filter_by(user_id=current_user.id).order_by(Footprint.date.desc()).first()
        new_footprint = Footprint.query.filter_by(user_id=current_user.id, id=10).first()
        if new_footprint:
            #current_date = datetime.now()
            #new_date = current_date - timedelta(days=30)  # Assuming a month is 30 days
            #new_footprint.date = new_date
            new_footprint.income_category = "Very High"
            db.session.commit()
            #new_footprint = Footprint.query.filter_by(user_id=current_user.id).order_by(Footprint.date.desc()).offset(1).limit(1).first()
            #new_footprint = Footprint.query.filter_by(user_id=current_user.id).order_by(Footprint.date.desc()).first()
            new_footprint = Footprint.query.filter_by(user_id=current_user.id, id=9).first()


            new_footprint_date = str(new_footprint.date)
            return render_template('mainmenu.html', message=new_footprint_date)
'''
