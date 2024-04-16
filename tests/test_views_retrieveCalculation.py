import pytest
from flask import session, url_for
from flask_login import login_user, logout_user
from datetime import datetime, timedelta
from unittest.mock import patch
from website.models import Users, Footprint
from website import db

@pytest.fixture(scope='function')
def auth_client(client, app):
    # Assuming test_user is already added in conftest.py and it is the only user
    with app.app_context():
        test_user = Users.query.first()  # Ensure the user exists
        login_user(test_user)  # Login the user
        yield client
        logout_user()  # Logout after each test

@patch('website.dashboard.calculation.calculate_carbon_footprint')
def test_retrieve_calculation(mock_calculate, auth_client, app):
    # Mock the calculate_carbon_footprint function to return controlled test data
    mock_calculate.return_value = {
        'electricity_emission_factor': 920.64,  # 450 kWh * 0.20496 kg CO2/kWh
        'heating_emission_factor': 36512,  # 200 kWh * 182.56 kg CO2/kWh
        'car_emission_factor': 70537.59,  # 1000 km * 0.16323 kg CO2/km * 4.3
        'flight_emission_factor': 470600,  # 2000 miles * 0.2353 kg CO2/mile
        'meat_and_dairy_emission_factor': 7662.5,  # 500 £ * 0.355 kg CO2/£ * 4.3
        'grocery_emission_factor': 5178,  # 300 £ * 0.332 kg CO2/£ * 4.3
        'goods_emission_factor': 6622,  # 400 £ * 0.385 kg CO2/£ * 4.3
        'services_emission_factor': 1198.2,  # 100 £ * 0.293 kg CO2/£ * 4.3
        'waste_emission_factor': 157.02765,  # 0.377 tonnes/person * 497.045 kg CO2/tonne
        'water_emission_factor': 795.48,  # 54 m^3/person * 0.177 kg CO2/m^3
        'household_size': 3,
        'income_category': 'High',
        'recycling_status': 'Yes',
        'total_carbon_footprint': 62208.82765,  # Sum of all emissions divided by household size
        'forecasted_annual_footprint': 746506.1918,  # Total monthly footprint * 12
        'regional_annual_average_per_person': 6500,
        'UK_annual_average_per_person': 6000
    }

    # Form data simulating a POST request
    form_data = {
        'electricity': '450',
        'heating': '200',
        'heatingType': 'gas',
        'carMileage': '1000',
        'carType': 'petrol',
        'flight': '2000',
        'meatAndDairy': '500',
        'grocery': '300',
        'goods': '400',
        'services': '100',
        'householdIncome': '55000',
        'householdSize': '3',
        'recycling': 'Yes',
        'region': 'UK'
    }

    with app.app_context():
        response = auth_client.post('/retrieveCalculation', data=form_data)

    assert response.status_code == 302 #redirect
    assert Footprint.query.count() == 1
