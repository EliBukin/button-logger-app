import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Button Logger' in rv.data
