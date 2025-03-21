from typing import Optional
from datetime import date
from pydantic import BaseModel, field_validator

from .constants import VALID_GENRES


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

    @field_validator('title')
    def validate_title(cls, v):
        if not v or v.strip() == '':
            raise ValueError('Title cannot be empty')
        return v
    
    @field_validator('published_year')
    def validate_published_year(cls, v):
        current_year = date.today().year
        if v < 1800 or v > current_year:
            raise ValueError(f'Published year must be between 1800 and {current_year}')
        return v
    
    @field_validator('genre')
    def validate_genre(cls, v):
        if v not in VALID_GENRES:
            raise ValueError(f"Genre '{v}' is not valid. Must be one of: {', '.join(VALID_GENRES)}")
        return v

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
    genre: Optional[str] = None
    published_year: Optional[int] = None

    @field_validator('title')
    def validate_title(cls, v):
        if not v or v.strip() == '':
            raise ValueError('Title cannot be empty')
        return v
    
    @field_validator('published_year')
    def validate_published_year(cls, v):
        current_year = date.today().year
        if v < 1800 or v > current_year:
            raise ValueError(f'Published year must be between 1800 and {current_year}')
        return v
    
    @field_validator('genre')
    def validate_genre(cls, v):
        if v not in VALID_GENRES:
            raise ValueError(f"Genre '{v}' is not valid. Must be one of: {', '.join(VALID_GENRES)}")
        return v

class BookResponse(BaseModel):
    id: int
    title: str
    genre: str
    author_id: int
    published_year: int

    class Confing:
        from_attributes = True
