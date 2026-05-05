####### LIBRARIES #######
import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from recipes import router

####### GLOBAL VARIABLES #######
app = FastAPI()


####### API METHODS #######
@app.exception_handler(HTTPException)
async def customer_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "Success": False,
            "Error code:": exc.status_code,
            "Reason:": exc.detail,
            "Help:": "Please check yout request and try again.",
        },
    )


app.include_router(router)
