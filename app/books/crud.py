import csv, json

from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional


def create_author(db: Session, name: str):
    sql = """
    INSERT INTO authors (name) VALUES (:name) RETURNING id;
    """
    result = db.execute(text(sql), {'name': name})
    db.commit()
    return result.scalar()


def create_book(db: Session, title: str, author_id: int, genre: str, published_year: int):
    sql = """
    INSERT INTO books (title, author_id, genre, published_year)
    VALUES (:title, :author_id, :genre, :published_year)
    RETURNING id;
    """
    result = db.execute(text(sql), {
        'title': title, 
        'author_id': author_id,
        'genre': genre, 
        'published_year': published_year
    })
    
    db.commit()
    return result.scalar()


def get_books(db: Session, title: Optional[str], author: Optional[str], genre: Optional[str], 
              year_min: Optional[int], year_max: Optional[int], page: int, limit: int):
    sql = """
    SELECT books.id, books.title, books.genre, books.published_year, authors.id AS author_id
    FROM books
    JOIN authors ON books.author_id = authors.id
    WHERE (:title IS NULL OR books.title ILIKE '%' || :title || '%')
    AND (:author IS NULL OR authors.name ILIKE '%' || :author || '%')
    AND (:genre IS NULL OR books.genre ILIKE '%' || :genre || '%')
    AND (:year_min IS NULL OR books.published_year >= :year_min)
    AND (:year_max IS NULL OR books.published_year <= :year_max)
    ORDER BY published_year
    LIMIT :limit OFFSET :offset;
    """

    result = db.execute(text(sql), {
        'title': title,
        'author': author,
        'genre': genre,
        'year_min': year_min,
        'year_max': year_max,
        'limit': limit,
        'offset': (page - 1) * limit
    })
    books = result.fetchall()

    return [
        {
            'id': book.id,
            'title': book.title,
            'author_id': book.author_id,
            'genre': book.genre,
            'published_year': book.published_year,
        }
        for book in books
    ]


def get_book_by_id(db: Session, book_id: int):
    sql = """
    SELECT books.id, books.title, books.genre, books.published_year, authors.id AS author_id
    FROM books
    JOIN authors ON books.author_id = authors.id
    WHERE books.id = :book_id;
    """
    result = db.execute(text(sql), {'book_id': book_id})
    return result.fetchone()


def update_book(db: Session, book_id: int, title: Optional[str], genre: Optional[str], published_year: Optional[int]):
    sql = """
    UPDATE books
    SET title = COALESCE(:title, title),
        genre = COALESCE(:genre, genre),
        published_year = COALESCE(:published_year, published_year)
    WHERE id = :book_id
    RETURNING id    
    """
    result = db.execute(text(sql), {
        'book_id': book_id,
        'title': title,
        'genre': genre,
        'published_year': published_year,
    })
    db.commit()
    return result.scalar()


def delete_book(db: Session, book_id: int):
    sql = "DELETE FROM books WHERE id = :book_id;"
    result = db.execute(text(sql), {'book_id': book_id})
    db.commit()
    return result.rowcount > 0


def bulk_import_books(db: Session, file_path: str):
    books = []
    
    if file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            books = json.load(f)
    elif file_path.endswith('.csv'):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            books = [row for row in reader]
    
    sql = """
    INSERT INTO books (title, author_id, genre, published_year)
    VALUES (:title, :author_id, :genre, :published_year);
    """
    
    for book in books:
        db.execute(text(sql), book)
    
    db.commit()
    return len(books)
