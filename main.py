from fastapi import FastAPI
from app.routers.document_router import router as document_router
from app.db.database import engine
from app.models.document_model import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(document_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)