import pytest
from website.dashboard.calculation import *

'''
THESE UNIT TESTS TEST CARBON FOOTPRINT CALCULATION FUNCTION
'''

def test_conversion_factors():
    # Verify some key conversion factors
    assert conversion_factors['private_transport_petrol'] == 0.16323
    assert conversion_factors['electricity'] == 0.20496
    assert conversion_factors['water'] == 0.177

def test_categorise_income():
    assert categorise_income(20000) == 'Low'
    assert categorise_income(45000) == 'High'
    assert categorise_income(85000) == 'High'

# Define test cases
@pytest.mark.parametrize("response, expected_result", [

    ({
        'electricity': 100,
        'heating': 50,
        'heatingType': 'gas',
        'carMileage': 10000,
        'carType': 'petrol',
        'flight': 5000,
        'meatAndDairy': 100,
        'grocery': 200,
        'goods': 300,
        'services': 400,
        'householdIncome': 30000,
        'householdSize': 4,
        'region': 'UK',
        'recycling': 'Yes'
    }, {
        'electricity_emission_factor': 20.496,
        'heating_emission_factor': 9.128,
        'car_emission_factor':  7018.889999999999,
        'flight_emission_factor': 1176.5,
        'meat_and_dairy_emission_factor': 152.65,
        'grocery_emission_factor': 285.52000000000004,
        'goods_emission_factor':  496.65,
        'services_emission_factor': 503.9599999999999,
        'waste_emission_factor':  15.615497083333334,
        'water_emission_factor':  0.7965,
        'household_size': 4,
        'income_category': 'Average',
        'recycling_status': 'Yes',
        'total_carbon_footprint': pytest.approx(2420.051499270833, abs=0.01),
        'forecasted_annual_footprint': pytest.approx(29040.617991249997, abs=0.01),
        'regional_annual_average_per_person': 6500,
        'UK_annual_average_per_person': 6500
    })

])
def test_calculate_carbon_footprint(response, expected_result):
    # Call the function with the test input
    result = calculate_carbon_footprint(response, conversion_factors)

    # Check that the output matches the expected result
    assert result == expected_result
