from . import settings
# from database import Base, engine

class Settings:
    DB_USER=settings.DB_USER
    DB_PASSWORD=settings.DB_PASSWORD
    DB_HOST=settings.DB_HOST
    DB_PORT=settings.DB_PORT
    DB_NAME=settings.DB_NAME

class DBInitialize:
    
    @staticmethod
    def create_table(Base, engine):
        Base.metadata.create_all(engine)