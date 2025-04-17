from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="Diagnosix Auth Service")

app.include_router(auth.router)