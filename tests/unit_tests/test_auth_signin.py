import pytest
from website.models import Users
from flask_login import current_user
from website import db

def test_signin_success(client):
    # Create a test user

    # Attempt to sign in with the correct credentials for test_user
    with client:
        response = client.post('/signin', data={
            'email': 'test@example.com',
            'password': 'SecurePassword!',
        }, follow_redirects=True)

        assert response.status_code == 200
        assert current_user is not None

def test_signin_failure(client):
    # Attempt to sign in with incorrect password
    response = client.post('/signin', data={
        'email': 'test@example.com',
        'password': 'incorrectpassword',
    })

    assert response.status_code == 200
    assert b'Invalid email or password' in response.data
