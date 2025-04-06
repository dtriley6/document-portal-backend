from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./database.db"  # For SQLite async database
# DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"  # For Postgres async database

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
