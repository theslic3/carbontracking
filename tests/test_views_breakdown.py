import pytest
from unittest.mock import patch
from website.views import breakdown
from flask import session
from website import create_app

@pytest.fixture(scope='function')
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'secret_key'  # Add a secret key for session
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_breakdown(client):
    # Mock the session data
    with client.session_transaction() as sess:
        sess['monthly_footprint'] = {'data': 'mocked_monthly_footprint'}
        sess['graph_data'] = {'data': 'mocked_graph_data'}
        sess['response_improvements'] = {'data': 'mocked_response_improvements'}
        sess['response_discussion'] = {'data': 'mocked_response_discussion'}

    response = client.get('/breakdown')

    assert response.status_code == 302
