from fastapi import FastAPI
from app.database import Base, engine
from app.config.db_initialize import DBInitialize
from app.routes import user

class Start():

    @staticmethod
    def app_start():
        app = FastAPI()

        DBInitialize.create_table(Base, engine)

        app.include_router(user.router)

        return app