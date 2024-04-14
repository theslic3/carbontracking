import pytest
from unittest.mock import patch, MagicMock
from flask import url_for, session
from datetime import datetime, timedelta
from website.models import Users


def test_emission_factors_no_previous_footprint(logged_in_client):
    form_data = {
    'electricity_emission_factor': '100',
    'heating_emission_factor': '50',
    'car_emission_factor': '75',
    'flight_emission_factor': '120',
    'meat_and_dairy_emission_factor': '60',
    'grocery_emission_factor': '30',
    'goods_emission_factor': '45',
    'services_emission_factor': '25',
    'waste_emission_factor': '15',
    'water_emission_factor': '10',
    'household_size': '4',
    'income_category': 'High',
    'recycling_status': 'Yes',
    'total_carbon_footprint': '500',
    'forecasted_annual_footprint': '6000',
    'regional_annual_average_per_person': '5500',
    'UK_annual_average_per_person': '6500'
    }
    with patch('website.views.calculate_carbon_footprint', return_value=form_data), \
         patch('website.views.Footprint.query') as mock_query, \
         patch('website.views.db.session.add') as mock_add, \
         patch('website.views.db.session.commit') as mock_commit: \

        mock_query.filter_by.return_value.order_by.return_value.first.return_value = None  # No previous footprint
        response = authenticated_client.post(url_for('views.emissionFactors'), data=form_data)


        assert mock_add.called
        assert mock_commit.called
        assert "You have submitted your first emissions data! Visit breakdown to see your results!" in response.get_data(as_text=True)
        assert response.status_code == 200

def test_emission_factors_with_previous_footprint_validation_fail(logged_in_client):
    form_data = {
        'electricity_emission_factor': '100',
        'heating_emission_factor': '50',
        'car_emission_factor': '75',
        'flight_emission_factor': '120',
        'meat_and_dairy_emission_factor': '60',
        'grocery_emission_factor': '30',
        'goods_emission_factor': '45',
        'services_emission_factor': '25',
        'waste_emission_factor': '15',
        'water_emission_factor': '10',
        'household_size': '4',
        'income_category': 'High',
        'recycling_status': 'Yes',
        'total_carbon_footprint': '500',
        'forecasted_annual_footprint': '6000',
        'regional_annual_average_per_person': '5500',
        'UK_annual_average_per_person': '6500'
    }

    with patch('website.views.calculate_carbon_footprint') as mock_calculate, \
         patch('website.views.Footprint.query') as mock_query, \
         patch('website.views.validation', return_value=False) as mock_validation, \
         patch('website.views.db.session.commit') as mock_commit:

        # Configure the mock to simulate a recent previous footprint
        mock_footprint = MagicMock()
        mock_footprint.date = datetime.now() - timedelta(days=0)  # Only 10 days old
        mock_query.filter_by.return_value.order_by.return_value.first.return_value = mock_footprint


        response = authenticated_client.post(url_for('views.emissionFactors'), data=form_data, follow_redirects=True)
        assert 'potential_footprint' in session, "Session should contain 'potential_footprint'"
        assert response.status_code == 302, "Should redirect due to validation fail"

            # Optionally, check for the correct redirect endpoint if needed
        assert '/potential_overwrite' in response.headers['Location'], "Should redirect to the potential overwrite page"# Send POST request to the route


def test_emission_factors_with_previous_footprint_validation_pass(logged_in_client):
    form_data = {
    'electricity_emission_factor': '100',
    'heating_emission_factor': '50',
    'car_emission_factor': '75',
    'flight_emission_factor': '120',
    'meat_and_dairy_emission_factor': '60',
    'grocery_emission_factor': '30',
    'goods_emission_factor': '45',
    'services_emission_factor': '25',
    'waste_emission_factor': '15',
    'water_emission_factor': '10',
    'household_size': '4',
    'income_category': 'High',
    'recycling_status': 'Yes',
    'total_carbon_footprint': '500',
    'forecasted_annual_footprint': '6000',
    'regional_annual_average_per_person': '5500',
    'UK_annual_average_per_person': '6500'
    }
    with patch('website.views.calculate_carbon_footprint') as mock_calculate, \
         patch('website.views.Footprint.query') as mock_query, \
         patch('website.views.validation') as mock_validation, \
         patch('website.views.db.session.commit') as mock_commit:

        mock_footprint = MagicMock()
        mock_footprint.date = datetime.now()
        mock_calculate.return_value = form_data
        mock_query.filter_by.return_value.order_by.return_value.first.return_value = mock_footprint
        mock_validation.return_value = True

        response = authenticated_client.post(url_for('views.emissionFactors'), data=form_data)

        assert mock_calculate.called
        assert mock_commit.called
        assert 'New Monthly Footprint Succesfully calculated! Visit breakdown to see your results!' in response.get_data(as_text=True)
