from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse


def add(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc: RequestValidationError):
        error_format = {
            "status": "fail",
            "message": "Request Validation Error",
            "errors": []
        }
        field_list = []
        for error in exc.errors():
            field_error = {
                "type": error["type"],
                "location": error["loc"][0],
                "field": error["loc"][1],
                "message": error["msg"]
            }
            field_list.append(field_error)

        error_format["errors"] = field_list

        return JSONResponse(status_code=422, content=error_format)