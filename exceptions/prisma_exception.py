from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from prisma.errors import RecordNotFoundError

def add(app: FastAPI):
    @app.exception_handler(RecordNotFoundError)
    async def _handler(_request: Request, exc: RecordNotFoundError):
        error_format = {
            "status": "fail",
            "message": "Resource Not Found Error",
            "errors": []
        }

        #TODO: write better errors
                
        return JSONResponse(status_code=404, content=error_format)
