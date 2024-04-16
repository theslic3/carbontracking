import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from website import create_app
from website.models import Footprint
from website.dashboard.footprintValidation import *

class TestValidationFunction(unittest.TestCase):
    def test_validation_true(self):
        current_date = datetime.now()
        prev_date = current_date - timedelta(days=31)
        self.assertTrue(validation(current_date, prev_date))

    def test_validation_false(self):
        current_date = datetime.now()
        prev_date = current_date - timedelta(days=29)
        self.assertFalse(validation(current_date, prev_date))


class TestGetMostRecentFootprint(unittest.TestCase):
    def test_get_most_recent_footprint(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            with patch('website.models.Footprint.query') as mock_query:
                mock_footprint = MagicMock()
                mock_query.filter_by.return_value.order_by.return_value.first.return_value = mock_footprint
                result = get_most_recent_footprint(1)
                self.assertEqual(result, mock_footprint)

class TestGetFootprintEmissionFactors(unittest.TestCase):
    def test_get_footprint_emission_factors(self):
        mock_footprint = MagicMock(
            electricity_emission_factor=100,
            heating_emission_factor=200,
            car_emission_factor=300,
            flight_emission_factor=120,
            meat_and_dairy_emission_factor=60,
            grocery_emission_factor=30,
            goods_emission_factor=45,
            services_emission_factor=25,
            waste_emission_factor=15,
            water_emission_factor=10
        )
        result = get_footprint_emission_factors(mock_footprint)
        self.assertEqual(result['Electricity'], 100)


class TestGetThreeHighestEmissions(unittest.TestCase):
    def test_get_three_highest_emissions(self):
        emissions = {'a': 100, 'b': 200, 'c': 300, 'd': 400}
        result = get_three_highest_emissions(emissions)
        self.assertEqual(result, [['d', 400], ['c', 300], ['b', 200]])

class TestGetBreakdownFacts(unittest.TestCase):
    def test_get_breakdown_facts(self):
        mock_footprint = MagicMock(
            forecasted_annual_footprint=1000,
            total_carbon_footprint=500,
            regional_annual_average_per_person=5500,
            UK_annual_average_per_person=6500,
            income_category='High',
            recycling_status='Yes',
            household_size=4
        )
        result = get_breakdown_facts(mock_footprint)
        self.assertEqual(result['Forecasted Annual Footprint, based on your monthly footprint'], 1000)

class TestGetGraphData(unittest.TestCase):
    def test_get_graph_data(self):
        factors = {'Electricity': 100, 'Heating': 200}
        tracking = {datetime.now(): 300}
        result = get_graph_data(factors, tracking)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)  # Expecting four lists of data

if __name__ == '__main__':
    unittest.main()
