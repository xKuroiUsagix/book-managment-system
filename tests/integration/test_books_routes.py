import pytest

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.fixture
def auth_token():
    client.post('/auth/register', json={'username': 'testuser', 'password': 'securepassword'})
    response = client.post('/auth/login', data={'username': 'testuser', 'password': 'securepassword'})
    return response.json().get('access_token')

@pytest.fixture(scope='module')
def created_book(auth_token):
    response = client.post(
        '/books/',
        json={'title': 'Test Book', 'author_id': 1, 'genre': 'Fiction', 'published_year': 2023},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    return response.json().get('id')

def test_create_book(auth_token):
    response = client.post(
        '/books/',
        json={'title': 'Test Book', 'author_id': 1, 'genre': 'Fiction', 'published_year': 2023},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 201
    assert response.json()['message'] == 'Book created successfully'

def test_list_books():
    response = client.get('/books')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_book():
    response = client.get('/books/1')
    assert response.status_code == 200
    assert 'title' in response.json()

def test_update_book(auth_token):
    response = client.put(
        '/books/1',
        json={'title': 'Updated Book', 'genre': 'Fiction', 'published_year': 2024},
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    assert response.status_code == 200
    assert response.json()['message'] == 'Book updated successfully'

def test_delete_book(auth_token):
    response = client.delete('/books/1', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 204
