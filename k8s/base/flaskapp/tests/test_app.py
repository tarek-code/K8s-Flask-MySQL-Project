import pytest
from unittest.mock import patch, MagicMock
from k8s.base.flaskapp.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_healthz(client):
    resp = client.get('/healthz')
    assert resp.status_code == 200
    assert resp.data == b"OK"

@patch('k8s.base.flaskapp.app.get_connection')
def test_home_route(mock_get_conn, client):
    # Mock the cursor and its fetchone method
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {'count': 5}

    # Mock the connection's cursor() method to return our mock cursor
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    # Mock get_connection to return our mock connection
    mock_get_conn.return_value = mock_conn

    response = client.get('/')
    assert response.status_code == 200
    assert b"Counter: 5" in response.data

@patch('k8s.base.flaskapp.app.get_connection')
def test_flask_route(mock_get_conn, client):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {'count': 7}  # رقم مختلف عشان نميز الاختبار

    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_get_conn.return_value = mock_conn

    response = client.get('/flask')
    assert response.status_code == 200
    assert b"Counter: 7" in response.data
@patch('k8s.base.flaskapp.app.get_connection')
def test_increment_route(mock_get_conn, client):
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    response = client.post('/increment')
    assert response.status_code == 200
    # Expected redirect script in response
    assert b"window.location.href" in response.data

    # Verify that the update query was executed and commit called
    mock_cursor.execute.assert_called_with("UPDATE counter SET count = count + 1 WHERE id = 1;")
    mock_conn.commit.assert_called_once()

