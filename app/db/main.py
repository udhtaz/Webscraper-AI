from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import Config

def get_async_engine() -> AsyncEngine:
    """Return async database engine."""
    try:
        db_url = URL.create("postgresql+asyncpg",
            username=Config.DB_USERNAME,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            # sslmode=Config.DB_SSL 
            )
        
        async_engine: AsyncEngine = create_async_engine(
            db_url, echo = True,
            future=True,
        )
    except SQLAlchemyError as e:
        print("Unable to establish db engine, database might not exist yet")
        print(e)

    return async_engine

async def init_db() -> None:
    """Create table in metadata if they don't exist yet.
    
    This uses a sync connection because the 'create_all' doesn't
    feature async yet.
    """

    async_engine = get_async_engine()

    async with async_engine.begin() as async_conn:
        await async_conn.run_sync(SQLModel.metadata.create_all)
        print("Initializing database was successfull.")
        

async def get_session() -> AsyncSession:
    async_engine = get_async_engine()

    async_session = sessionmaker(
        bind=async_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session
