import pytest

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.fixture(scope='module')
def test_user():
    client.post('/auth/register', json={'username': 'testuser', 'password': 'securepassword'})

def test_register_user():
    response = client.post('/auth/register', json={'username': 'testuser', 'password': 'securepassword'})
    assert response.status_code == 201

def test_login_user():
    client.post('/auth/register', json={'username': 'testuser', 'password': 'securepassword'})

    response = client.post('/auth/login', data={'username': 'testuser', 'password': 'securepassword'})
    assert response.status_code == 200
    assert 'access_token' in response.json()

def test_login_with_wrong_credentials():
    response = client.post('/auth/login', data={'username': 'testuser', 'password': 'wrongpassword'})
    assert response.status_code == 401
