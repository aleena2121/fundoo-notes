from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.db_initialize import DBInitialize
from app.config.logger import config_logger
from app.database import Base, engine
from app.models.notes_model import Notes
from app.routes.auth import login_router, sign_up_router
from app.routes.notes import notes_router
from app.routes.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        DBInitialize.create_table(Base, engine)
        config_logger.info("Database created")
        yield
    except Exception as e:
        config_logger.error(f"Error during app startup: {e}")
        raise
    finally:
        config_logger.info("App shutdown")


app = FastAPI(lifespan=lifespan)
app.include_router(sign_up_router)
app.include_router(login_router)
app.include_router(user_router)
app.include_router(notes_router)
