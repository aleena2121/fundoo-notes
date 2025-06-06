from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import db_initialize


DB_USER=db_initialize.settings.DB_USER
DB_PASSWORD=db_initialize.settings.DB_PASSWORD
DB_HOST=db_initialize.settings.DB_HOST
DB_PORT=db_initialize.settings.DB_PORT
DB_NAME=db_initialize.settings.DB_NAME

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()