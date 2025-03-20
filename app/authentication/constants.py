import os


SECRET_KEY = os.getenv('JWT_SECRET', 'your_secret_key')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
