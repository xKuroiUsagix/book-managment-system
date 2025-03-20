import os

from typing import List, Optional

from fastapi import (APIRouter, Depends, File, UploadFile, HTTPException, status)
from sqlalchemy.orm import Session

from ..authentication.auth import get_current_user
from ..database import get_db
from .crud import (
    create_author, create_book, get_books, get_book_by_id, update_book, delete_book, bulk_import_books
)
from .schemas import (
    AuthorCreate, AuthorResponse, BookCreate, BookResponse, BookUpdate
)


router = APIRouter()


@router.post('/authors', response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def add_author(author: AuthorCreate, db: Session=Depends(get_db), user=Depends(get_current_user)):
    author_id = create_author(db, author.name)

    if not author_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Author could not be created'
        )
    return {'id': author_id, 'name': author.name, 'message': 'Author created successfully'}


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_book(book: BookCreate, db: Session=Depends(get_db), user=Depends(get_current_user)):
    book_id = create_book(db, book.title, book.author_id, book.genre, book.published_year)

    if not book_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Book could not be created'
        )
    return {'id': book_id, 'message': 'Book created successfully'}


@router.get('/', response_model=List[BookResponse], status_code=status.HTTP_200_OK)
def list_books(title: Optional[str] = None, 
               author: Optional[str] = None, 
               genre: Optional[str] = None, 
               year_min: Optional[int] = None, year_max: Optional[int] = None, 
               page: int = 1, limit: int = 10, 
               db: Session = Depends(get_db)):
    books = get_books(db, title, author, genre, year_min, year_max, page, limit)
    
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No books found'
        )
    return books


@router.get('/{book_id}', response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(db, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return book


@router.put('/{book_id}', status_code=status.HTTP_200_OK)
def edit_book(book_id: int, book: BookUpdate, db: Session=Depends(get_db), user=Depends(get_current_user)):
    updated_id = update_book(db, book_id, book.title, book.genre, book.published_year)

    if not updated_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return {'message': 'Book updated successfully'}


@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_book(book_id: int, db: Session=Depends(get_db), user=Depends(get_current_user)):
    is_deleted = delete_book(db, book_id)

    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return {'message': 'Book deleted successfully'}


@router.post('/import/', status_code=status.HTTP_200_OK)
def import_books(file: UploadFile = File(...), db: Session=Depends(get_db), user=Depends(get_current_user)):
    upload_dir = './uploads'
    
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = f'./uploads/{file.filename}'
    with open(file_path, 'wb') as f:
        f.write(file.file.read())

    count = bulk_import_books(db, file_path)
    if count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No books were imported'
        )
    return {'message': f'{count} books imported successfully'}
