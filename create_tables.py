from app.database import engine, Base
from app.books.models import *
from app.authentication.models import *

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
