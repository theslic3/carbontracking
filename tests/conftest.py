'''
import pytest
from flask import session, template_rendered
from contextlib import contextmanager
from datetime import datetime
from website import create_app, db
from website.models import Footprint, Users
'''


import os
from website.models import Users
from flask_login import login_user

@pytest.fixture(scope='module')
def app():
    os.environ['FLASK_ENV'] = 'testing'
    _app = create_app()
    ctx = _app.app_context()
    ctx.push()
    with ctx:
        db.create_all()

    test_user = Users(
        email='test@example.com',
        name='Test User',
        password='SecurePassword!'
    )
    db.session.add(test_user)
    db.session.commit()


    yield _app
    with ctx:
        db.session.remove()
        db.drop_all()
    ctx.pop()
    os.environ['FLASK_ENV'] = 'development'

@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""
    return app.test_client()

'''
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()


    test_user = Users(
        email='test@example.com',
        name='Test User',
        password='SecurePassword!'
    )
    db.session.add(test_user)
    db.session.commit()


    yield client

    with app.app_context():

        db.drop_all()

@pytest.fixture
def logged_in_client(client):
    with client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1  # Assume the user ID of the logged-in user is 1
    return client

def test_emission_factors_no_previous_footprint(logged_in_client):
    response_data = {
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
        # Include all other factors...
    }
    with logged_in_client as c:
        response = c.post('/retrieveCalculation', data=response_data)
        assert response.status_code == 200
        assert "You have submitted your first emissions data!" in response.get_data(as_text=True)

        # Check if the Footprint object is created
        footprint = Footprint.query.first()
        assert footprint is not None
        assert footprint.electricity_emission_factor == '123'
        assert footprint.heating_emission_factor == '456'
'''
