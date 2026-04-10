from fastapi import FastAPI

from routes.api import router
from middlewares import cors_middleware
from exceptions import prisma_exception, validation_exception
from utilities.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

validation_exception.add(app=app)
prisma_exception.add(app=app)

cors_middleware.add(app=app)

app.include_router(router)
