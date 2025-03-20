from typing import Optional
from datetime import date

from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException


class AuthorCreate(BaseModel):
    name: str

class AuthorResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class BookCreate(BaseModel):
    title: str
    genre: str
    author_id: int
    published_year: int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    genre: Optional[str] = None
    published_year: Optional[int] = None

class BookResponse(BaseModel):
    id: int
    title: str
    genre: str
    author_id: int
    published_year: int

    class Confing:
        from_attributes = True
