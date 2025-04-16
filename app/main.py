from fastapi import FastAPI
from app.routers import auth
from app.db import engine, Base

app = FastAPI(title="Diagnosix Auth Service")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)