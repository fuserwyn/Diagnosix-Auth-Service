from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.routers import auth
from app.utils.exceptions import validation_exception_handler

app = FastAPI(title="Diagnosix Auth Service")
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(auth.router)
