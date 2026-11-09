from contextlib import asynccontextmanager

from fastapi import FastAPI

from my_project.api.routes import ask, items
from my_project.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # create tables on startup
    yield


app = FastAPI(title="my-project", lifespan=lifespan)
app.include_router(items.router)
app.include_router(ask.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
