from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from core.settings import settings
from db.db_helper import db_helper
from models.base import Base
from api.v1.routes.user_router import router as jwt_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(jwt_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
