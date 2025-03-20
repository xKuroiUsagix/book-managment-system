from fastapi import FastAPI

from app.books.routes import router as books_router
from app.authentication.routes import router as auth_router


app = FastAPI()
app.include_router(books_router, prefix='/books')
app.include_router(auth_router, prefix='/auth')
