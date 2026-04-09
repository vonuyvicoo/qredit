from fastapi import FastAPI

from routes.api import router
from middlewares import cors_middleware
from exceptions import validation_exception

app = FastAPI()

# Add Error Handler for Request Validation
validation_exception.add(app=app)

# Add Middlewares
cors_middleware.add(app=app)

#  Add Router to app
app.include_router(router)
