import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_healthz(client):
    rv = client.get('/healthz')
    assert rv.status_code == 200
    assert rv.data == b"OK"

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Counter" in rv.data

def test_flask_route(client):
    rv = client.get('/flask')
    assert rv.status_code == 200
    assert b"Counter" in rv.data

