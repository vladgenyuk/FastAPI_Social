import os

from dotenv import load_dotenv


load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

REDIS_HOST = os.environ.get('REDIS_HOST')

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
JWT_EXPIRATION_TIME_SECONDS = int(os.environ.get('JWT_EXPIRATION_TIME_SECONDS'))


GIT_CLIENT_ID = os.environ.get('GIT_CLIENT_ID')
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')

GIT_SECRET = os.environ.get('GIT_SECRET')
GOOGLE_SECRET = os.environ.get('GOOGLE_SECRET')

EMAIL_CHECK_API_KEY = os.environ.get('EMAIL_CHECK_API_KEY')

OAUTH_SECRET_PASSWORD = os.environ.get('OAUTH_SECRET_PASSWORD')

