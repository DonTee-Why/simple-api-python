from typing import Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from main import app

class ApiException(HTTPException):
    def __init__(self, code: int, detail: Any = None):
        self.status_code = code
        self.detail = detail

@app.exception_handler(ApiException)
def api_exception_handler(request: Request, ex: ApiException):
    return JSONResponse(
        status_code=ex.status_code,
        content={"status_code": f"{ex.status_code}", "message": f"{ex.detail}"}
    )