from fastapi import FastAPI

from app.config.db_initialize import DBInitialize
from app.database import Base, engine
from app.routes import auth, user


class Start():

    @staticmethod
    def app_start():
        app = FastAPI()

        DBInitialize.create_table(Base, engine)

        app.include_router(user.router)
        app.include_router(auth.router)

        return app