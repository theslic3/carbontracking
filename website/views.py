from datetime import datetime, date, timedelta
from .models import Users, Test, Footprint
from . import db
from flask import Blueprint, render_template, request, jsonify, Response, redirect, flash, url_for, session
from flask_login import login_required, current_user
from website.dashboard.calculation import *
from website.dashboard.footprintValidation import *
from website.dashboard.improvementGeneration import *
import json


views = Blueprint('views', __name__)

@views.route('/mainmenu', methods=['GET', 'POST'])
@login_required
def show_dashboard():
    return render_template('mainmenu.html') #,user=current_user

@views.route('/faq', methods=['GET'])
@login_required
def faq():
    return render_template('faq.html')

@views.route('/lifestyle', methods=['GET', 'POST'])
@login_required
def inputs():
    return render_template('lifestyle.html')

@views.route('/retrieveCalculation', methods= ['POST'])
@login_required
def emissionFactors():
    response = request.form
    footprint_profile = calculate_carbon_footprint(response, conversion_factors)
    data = {}
    for factor in footprint_profile: #Dictionary of footprint data to be validated against, filled out
        data[factor] = footprint_profile[factor]

    #create a footprint object, ready to be commited for validated footprints, using the footprint_profile dictionary
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
            db.session.add(new_footprint) #if validated, add the footprint object to db
            db.session.commit()
            return render_template('mainmenu.html', message="New Monthly Footprint Succesfully calculated! Visit breakdown to see your results! ")
        else:
            session['potential_footprint'] = data #if a previous footprint < 30 days old is found, redirect for permission to overwrite the current
            return redirect('/potential_overwrite')

    db.session.add(new_footprint) # If no previous footprint,  add the new footprint to the database
    db.session.commit()
    return render_template('mainmenu.html', message="You have submitted your first emissions data! Visit breakdown to see your results! ")


@views.route('/potential_overwrite', methods=['GET'])
@login_required
def potential_overwrite():
    return render_template('lifestyle.html', warning='Potential Overwrite') #Rendering the template with this warning will cause a JS alert to prompt for permission to overwrtie footprint

@views.route('/overwrite', methods=['GET'])  #If yes is prompted, from the lifestyle template, the footprint will be overwritten, by routing here
@login_required
def overwrite():
    footprint_profile = session.get('potential_footprint') #retrieve footprint dictionary from session
    response = request.args.get('response')
    new_footprint = Footprint( #generate footprint object using the session dictionary
        user_id=current_user.id,
        date=datetime.now().date(),
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
        return render_template('mainmenu.html', message="Monthly Footprint Overwritten. Visit breakdown to see your results! ")  # Redirect to main menu after overwriting
    elif response == 'no':
        return render_template('mainmenu.html', message="No changes")  # Redirect to main menu without overwriting
    else:
        return redirect('/mainmenu')

@views.route('/retrieve_emissionfactors', methods=['GET', 'POST'])
@login_required
def retrieve():
    try:
        most_recent_footprint = get_most_recent_footprint(current_user.id)
        if not most_recent_footprint:
            raise ValueError("No recent footprint found.")

        emission_factors_recent = get_footprint_emission_factors(most_recent_footprint)
        three_highest_emissions = get_three_highest_emissions(emission_factors_recent)
        footprint_breakdown_facts = get_breakdown_facts(most_recent_footprint)
        footprints_with_dates = get_previous_footprints_with_dates(current_user.id)
        graph_data = get_graph_data(emission_factors_recent, footprints_with_dates)

        print(three_highest_emissions)
        print(footprint_breakdown_facts)

        improvements = generate_lifestyle_improvements_prompt(footprint_breakdown_facts, three_highest_emissions)
        discussion = generate_footprint_discussion_prompt(footprint_breakdown_facts)

        response_improvements = generate_suggestions(improvements)
        response_discussion = generate_suggestions(discussion)

        session['monthly_footprint'] = int(most_recent_footprint.total_carbon_footprint)
        session['graph_data'] = graph_data
        session['response_improvements'] = response_improvements
        session['response_discussion'] = response_discussion
        return redirect('/breakdown')

    except ValueError as e:
        return render_template('mainmenu.html', message="No previous footprint data found- Add some!")
    except Exception as e:
        return render_template('mainmenu.html', message="An error occurred. Please try again later.")

@views.route('/breakdown', methods=['GET', 'POST'])
@login_required
def breakdown():
    monthly_footprint = session.get('monthly_footprint')
    graph_data = session.get('graph_data')
    response_improvements = session.get('response_improvements')
    response_discussion = session.get('response_discussion')

    return render_template('visualise.html', graph_data=graph_data, improvements=response_improvements, discussion=response_discussion, fp = monthly_footprint)


@views.route('/account')
@login_required
def account():
    return render_template('account.html')

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('mainmenu.html', message="Account Changed")

'''
#ADMIN USE ONLY - FOR MANUAL DATABASE EDITS
@views.route('/testingdates', methods=['GET', 'POST'])
@login_required
def datetest():
    #previous_footprint = Footprint.query.filter_by(user_id=current_user.id).order_by(Footprint.date.desc()).first()
    new_footprint = Footprint.query.filter_by(user_id=current_user.id, id=6).first()
    if new_footprint:
        seven_months_ago = datetime.now() - timedelta(days=30*2)
        new_footprint.date = seven_months_ago
        db.session.commit()
        return render_template('mainmenu.html', message=seven_months_ago)
'''
