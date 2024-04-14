import pytest
from website import create_app, db
from website.models import Users
from flask_login import current_user


def test_register(client):
    # Test successful registration
    response = client.post('/register', data={
        'email': 'test@gmail.com',
        'name': 'Testingg',
        'password1': 'SecurePassword!09',
        'password2': 'SecurePassword!09',
    }, follow_redirects=True)


    assert response.status_code == 200
    assert Users.query.count() == 2 #number of users is now two, after adding new user
    assert current_user is not None #should be a current user, after registration


    # Test registration with existing email
    response = client.post('/register', data={
        'email': 'test@gmail.com',
        'name': 'Testing',
        'password1': 'AnotherPassword!09',
        'password2': 'AnotherPassword!09',
    })
    assert b'Email already exists' in response.data
