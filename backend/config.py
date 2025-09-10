import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL", None)
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    AZURE_CONTAINER = os.getenv("AZURE_CONTAINER", "attachments")
