from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-creates tables in PostgreSQL on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="ATS Analyzer", lifespan=lifespan)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "ATS Analyzer API is running"}