import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Reemplaza 'user', 'password' y 'database_name' con tus credenciales de MySQL..
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@127.0.0.1:3306/database_name"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()