from fastapi import FastAPI
from app.database import Base, engine, get_db
from app.config.db_initialize import DBInitialize
from app.routes import user

app = FastAPI()

DBInitialize.create_table(Base, engine)

app.include_router(user.router)