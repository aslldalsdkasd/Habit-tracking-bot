import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import inspect
from fastapi_client.database.conection import engine, init_db
from fastapi_client.database.model import Base
from fastapi_client.routes.routes import router
from logging.config import dictConfig
from logger_conf import LOGGER
dictConfig(LOGGER)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("таблицы созданы")

    yield

    await engine.dispose()
    logger.info("дб закрыто")


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/")
async def index():
    return "hello"
