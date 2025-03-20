from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm


from .schemas import UserCreate, UserResponse, Token
from .crud import create_user, get_user_by_username
from .auth import create_access_token, authenticate_user
from ..database import get_db


router = APIRouter()


@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail='Username already registered')
    
    new_user = create_user(db, user.username, user.password)
    return new_user

@router.post('/login', response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_access_token(data={'sub': user.username}, expires_delta=timedelta(minutes=30))
    return {'access_token': access_token, 'token_type': 'bearer'}
