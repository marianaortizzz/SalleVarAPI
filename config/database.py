import os
from urllib.parse import urlparse, urlunparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DEFAULT_DATABASE_URL = "mysql://root:root@127.0.0.1:3306/sallevar"

SQLALCHEMY_DATABASE_URL_FULL = os.environ.get(
    "DATABASE_URL",
    DEFAULT_DATABASE_URL
)

parsed_url = urlparse(SQLALCHEMY_DATABASE_URL_FULL)
SQLALCHEMY_DATABASE_URL = urlunparse(parsed_url._replace(query=''))

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=True,
    connect_args={
        'ssl': {
            'ssl_mode': 'REQUIRED'
        }
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()