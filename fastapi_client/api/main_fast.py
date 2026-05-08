from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import inspect
from fastapi_client.database.conection import engine, init_db
from fastapi_client.routes.classCRUD import router

app = FastAPI()
app.include_router(router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    inspector = inspect(engine.sync_engine)

    tables = ['habits', 'user_habits']
    missing = []
    for table in tables:
        if not inspector.has_table(table):
            missing.append(table)

    if missing:
        print(f'нету {missing}')
        await init_db()
        print('инициализирована')

    yield

    await engine.dispose()
    print('db закрыта')

@app.get('/')
async def index():
    return 'hello'