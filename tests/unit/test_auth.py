import pytest

from datetime import timedelta
from jose import jwt

from app.authentication.utils import hash_password, verify_password
from app.authentication.auth import create_access_token
from app.authentication.constants import SECRET_KEY, ALGORITHM


def test_hash_password():
    password = 'securepassword'
    hashed = hash_password(password)
    assert hashed != password

def test_verify_password():
    password = 'securepassword'
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password('wrongpassword', hashed)

def test_create_access_token():
    data = {'sub': 'testuser'}
    token = create_access_token(data, expires_delta=timedelta(minutes=30))
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_data['sub'] == 'testuser'
