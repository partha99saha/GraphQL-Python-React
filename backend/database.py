from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
SessionLocal = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
