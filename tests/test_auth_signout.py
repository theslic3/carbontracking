import pytest
from flask import url_for
from flask_login import current_user
from website.models import Users, Footprint

def test_signout_authenticated_user(client, app):
    """
    Test that an authenticated user is logged out and redirected to the sign-in page.
    """
    # Log in the user first
    with client:
        with app.app_context():
            # Assuming `login_user(test_user)` would typically happen here
            test_user = Users.query.first()
            # Using Flask-Login to log in the user
            from flask_login import login_user
            login_user(test_user)

            assert current_user.is_authenticated == True

            # Now, hit the signout route
            response = client.get(url_for('auth.signout'), follow_redirects=False)

            # Check that the response is a redirect to the /signin page
            assert response.status_code == 302
            assert '/signin' in response.headers['Location']

            # Ensure the user is logged out
            assert current_user.is_authenticated == False

def test_signout_unauthenticated_user(client, app):
    """
    Test that an unauthenticated user who tries to signout is redirected properly,
    potentially after being handled by the login_required decorator.
    """
    with client:
        response = client.get(url_for('auth.signout'), follow_redirects=False)
        assert response.status_code == 302
