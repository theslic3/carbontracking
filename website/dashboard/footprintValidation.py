from datetime import datetime, timedelta
from website.models import Footprint
from flask_login import current_user

def validation(current_date, prev_date):
    time_difference = current_date - prev_date
    days_difference = time_difference.days
    if days_difference >= 30:
        return True
    else:
        return False
    #flash('Your previous footprint will be overwritten if you submit a new one. Do you want to proceed?', category='warning')

def plus_one_month(current_date, num_days):
    #Call in prgram by plus_one_month(datetime.now(), 30)
    new_date = current_date - timedelta(days = numDays)
    return new_date

'''
def new_footprint(footprint_profile):
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

    return new_footprint
'''
