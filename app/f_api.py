# from contextlib import asynccontextmanager

# from fastapi import FastAPI

# from app.config.db_initialize import DBInitialize
# from app.config.logger import config_logger
# from app.database import Base, engine
# from app.models.notes_model import Notes
# from app.routes.auth import login_router, sign_up_router
# from app.routes.notes import notes_router
# from app.routes.user import router as user_router
# from app.routes.labels import label_router
# from app.middlewares.request_logger import RequestCountMiddleware
# from sqlalchemy.orm import configure_mappers

# from app.models import user_model, labels_model, notes_model, association

# configure_mappers()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     try:
#         DBInitialize.create_table(Base, engine)
#         config_logger.info("Database created")
#         yield
#     except Exception as e:
#         config_logger.error(f"Error during app startup: {e}")
#         raise
#     finally:
#         config_logger.info("App shutdown")


# app = FastAPI(lifespan=lifespan)
# app.include_router(sign_up_router)
# app.include_router(login_router)
# app.include_router(user_router)
# app.include_router(notes_router)
# app.include_router(label_router)

# app.add_middleware(RequestCountMiddleware)


from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config.db_initialize import DBInitialize
from app.config.logger import config_logger
from app.database import Base, engine
from app.models.notes_model import Notes
from app.routes.auth import login_router, sign_up_router
from app.routes.notes import notes_router
from app.routes.user import router as user_router
from app.routes.labels import label_router
from app.middlewares.request_logger import RequestCountMiddleware
from sqlalchemy.orm import configure_mappers
import app.models

configure_mappers()


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
app.add_middleware(RequestCountMiddleware)
app.include_router(sign_up_router)
app.include_router(login_router)
app.include_router(user_router)
app.include_router(notes_router)
app.include_router(label_router)
