import os

from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
CMC_API_KEY = os.environ.get("CMC_API_KEY")
DB_NAME = os.environ.get("DB_NAME")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PORT = os.environ.get("DB_PORT")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_HOST = os.environ.get("REDIS_HOST")
