from datetime import datetime, timedelta
from website.models import Footprint
from flask_login import current_user
from  .. import db

def validation(current_date, prev_date):
    time_difference = current_date - prev_date
    days_difference = time_difference.days
    if days_difference >= 30:
        return True
    else:
        return False
    #flash('Your previous footprint will be overwritten if you submit a new one. Do you want to proceed?', category='warning')

#This is used by admin function to manually edit dates in db
def plus_one_month(current_date, num_days):
    #Call in prgram by plus_one_month(datetime.now(), 30)
    new_date = current_date - timedelta(days = numDays)
    return new_date

def get_most_recent_footprint(user_id):
    most_recent_footprint = Footprint.query.filter_by(user_id=user_id).order_by(Footprint.date.desc()).first()
    return most_recent_footprint

# Accessing emission factors directly from the most recent footprint object
def get_footprint_emission_factors(most_recent_footprint):
        # Accessing emission factors directly from the most recent footprint object
    emissions_factors = {
        'Electricity': most_recent_footprint.electricity_emission_factor,
        'Home Heating': most_recent_footprint.heating_emission_factor,
        'Car': most_recent_footprint.car_emission_factor,
        'Air Travel': most_recent_footprint.flight_emission_factor,
        'Meat and Dairy': most_recent_footprint.meat_and_dairy_emission_factor,
        'Rest of Grocery shop': most_recent_footprint.grocery_emission_factor,
        'Purchases of non-essential items': most_recent_footprint.goods_emission_factor,
        'Services': most_recent_footprint.services_emission_factor,
        'Waste Disposal': most_recent_footprint.waste_emission_factor,
        'Water Usage': most_recent_footprint.water_emission_factor
    }
    return emissions_factors

# Retrieve up to 6 previous footprints with dates, for use for tracking
def get_previous_footprints_with_dates(user_id):
    # Retrieve up to 6 previous footprints with dates, for use for tracking
    previous_footprints = Footprint.query.filter_by(user_id=user_id).order_by(Footprint.date.desc()).limit(6).all()
    footprints_with_dates = {}

    for footprint in previous_footprints:
        footprints_with_dates[footprint.date] = footprint.forecasted_annual_footprint

    return footprints_with_dates

#Retrieve 3 highest emissions, in a list, for use for lifestyle improvements
def get_three_highest_emissions(emissions):
    sorted_emissions = sorted(emissions.items(), key=lambda x: x[1], reverse=True)
    top_three = sorted_emissions[:3]
    result = [[key, value] for key, value in top_three]
    return result

def get_breakdown_facts(most_recent_footprint):
    breakdown_facts = {
        'Forecasted Annual Footprint, based on your monthly footprint': most_recent_footprint.forecasted_annual_footprint,
        'Your monthly carbon footprint, in terms of KG of CO released': most_recent_footprint.total_carbon_footprint,
        'Average Annual Footprint per person in your region': most_recent_footprint.regional_annual_average_per_person,
        'Average Annual Footprint per person in the UK ': most_recent_footprint.UK_annual_average_per_person,
        'Your houeshold disposable income categorises you as': most_recent_footprint.income_category,
        'Your Recycling Status': most_recent_footprint.recycling_status,
        'Your Household Size': most_recent_footprint.household_size
    }
    return breakdown_facts

#RETURN A LIST OF LISTS, SO CAN BE USED AS JSON DATA FOR THE GRAPH
def get_graph_data(factors, tracking):
    data_factors_key = []
    data_factors_value = []
    data_tracking_key = []
    data_tracking_value = []

    for factor in factors:
        data_factors_key.append(factor)
        data_factors_value.append(factors[factor])

    for date in tracking:
        data_tracking_key.append(date)
        data_tracking_value.append(tracking[date])

    formatted_dates = []

    # Reformatting dates into dd/mm/yyyy
    for date in data_tracking_key:
        formatted_date = date.strftime('%d/%m/%Y')         # Format the date as dd/mm/yyyy
        formatted_dates.append(formatted_date)

    #formatted_keys_factors = format_list_items(data_factors_key)

    return [data_factors_key, data_factors_value, formatted_dates, data_tracking_value]
