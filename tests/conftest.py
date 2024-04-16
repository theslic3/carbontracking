import os
import pytest
from datetime import datetime
from website import create_app, db
from website.models import Users, Footprint

@pytest.fixture(scope='module')
def app():
    """Create and configure a new app instance for each test."""
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    ctx = app.app_context()
    ctx.push()

    db.create_all()

    test_user = Users(email='test@example.com', name='Test User', password='SecurePassword!')
    db.session.add(test_user)
    db.session.flush()  # Flush to assign an ID to test_user

    new_footprint = Footprint(
        user_id=test_user.id,
        date=datetime.now().date(),
        electricity_emission_factor=4342,
        heating_emission_factor=4342,
        car_emission_factor=4343,
        flight_emission_factor=4342,
        meat_and_dairy_emission_factor=434,
        grocery_emission_factor=434,
        goods_emission_factor=434,
        services_emission_factor=3424,
        waste_emission_factor=3434,
        water_emission_factor=324,
        household_size=2,
        income_category='High',
        recycling_status="Yes",
        total_carbon_footprint=1240,
        forecasted_annual_footprint=3672,
        regional_annual_average_per_person=6500,
        UK_annual_average_per_person=6500
    )

    db.session.add(new_footprint)
    db.session.commit()

    yield app  # Yield the app for testing

    db.session.remove()
    db.drop_all()
    ctx.pop()
    os.environ['FLASK_ENV'] = 'development'

@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""
    return app.test_client()
