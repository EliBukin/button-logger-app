# tests/test_app.py

import pytest
from app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"BLA Logo" in response.data

def test_button_click(client):
    response = client.post('/button_click')
    assert response.status_code == 200
    assert b"Button clicked!" in response.data