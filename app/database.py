from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# PostgreSQL async engine
engine = create_async_engine(
    settings.database_url,
    echo=True,          # logs all SQL — helpful for debugging, turn off in production
    pool_size=5,
    max_overflow=10
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session