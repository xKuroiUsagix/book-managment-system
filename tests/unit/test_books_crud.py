import pytest

from app.books.crud import create_book, get_book_by_id, delete_book
from sqlalchemy.orm import Session
from unittest.mock import MagicMock


@pytest.fixture
def db_session():
    return MagicMock(spec=Session)

def test_create_book(db_session):
    db_session.add.return_value = None
    db_session.commit.return_value = None
    db_session.refresh.return_value = None

    book_id = create_book(db_session, 'Test Book', 1, 'Fiction', 2023)
    assert book_id is not None

def test_get_book_by_id(db_session):
    db_session.execute.return_value.fetchone.return_value = (1, 'Test Book', 1, 'Fiction', 2023)
    fetched_book = get_book_by_id(db_session, 1)
    assert 'Test Book' in fetched_book

def test_delete_book(db_session):
    db_session.execute.return_value.rowcount = 1

    is_deleted = delete_book(db_session, 1)
    assert is_deleted
