from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URI_AUTH')
# if SQLALCHEMY_DATABASE_URL is None:
SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # {
    #     "check_some_thread":False
    # }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()