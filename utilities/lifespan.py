from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.config import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()
