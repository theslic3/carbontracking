import pytest
from flask_login import login_user, logout_user
from website.models import Users, Footprint

def test_overwrite_yes(client, app):
    # Setup and teardown for each test will be managed by the fixtures in 'conftest.py'

    # Log in the user
    with app.app_context():
        test_user = Users.query.filter_by(email='test@example.com').first()
        login_user(test_user)

        # Add a potential footprint to the session
        with client.session_transaction() as sess:
            sess['potential_footprint'] = Footprint.query.filter_by(user_id=test_user.id).first().to_dict()

        # Send a GET request to the overwrite route with a 'yes' response
        response = client.get('/overwrite?response=yes')

        # Check that the correct message is returned
        assert 'Monthly Footprint Overwritten.' in response.get_data(as_text=True)
        # Ensure that only one footprint exists after the overwrite
        assert Footprint.query.count() == 1

        # Logout the user after the test
        logout_user()

def test_overwrite_no(client, app):
    # Log in the user
    with app.app_context():
        test_user = Users.query.filter_by(email='test@example.com').first()
        login_user(test_user)

        # Send a GET request to the overwrite route with a 'no' response
        response = client.get('/overwrite?response=no')

        # Check that the correct message is returned
        assert 'No changes' in response.get_data(as_text=True)
        # Ensure that the footprint was not overwritten
        assert Footprint.query.filter_by(user_id=test_user.id).count() == 1

        # Logout the user after the test
        logout_user()

def test_overwrite_unexpected_response(client, app):
    # Log in the user
    with app.app_context():
        test_user = Users.query.filter_by(email='test@example.com').first()
        login_user(test_user)

        # Send a GET request to the overwrite route with an unexpected response
        response = client.get('/overwrite?response=maybe')

        # Check that the user is redirected to the main menu
        assert response.status_code == 302
        assert '/mainmenu' in response.headers['Location']

        # Logout the user after the test
        logout_user()
