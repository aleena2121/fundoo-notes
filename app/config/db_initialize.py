from app.config.settings import dbsettings


class Settings:
    DB_USER = dbsettings.DB_USER
    DB_PASSWORD = dbsettings.DB_PASSWORD
    DB_HOST = dbsettings.DB_HOST
    DB_PORT = dbsettings.DB_PORT
    DB_NAME = dbsettings.DB_NAME


class DBInitialize:

    @staticmethod
    def create_table(Base, engine):
        Base.metadata.create_all(engine)
