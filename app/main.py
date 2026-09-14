from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="DevFlow API Engine",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(tasks.router)