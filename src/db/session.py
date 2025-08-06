from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from ..core.config import settings as s

load_dotenv()


url = (f"{s.POSTGRES_USER}:{s.POSTGRES_PASSWORD}@"
       f"{s.POSTGRES_HOST}:{s.POSTGRES_PORT}/{s.POSTGRES_DB}")

DATABASE_URL_ASYNC = f"postgresql+asyncpg://{url}"

engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный движок"""
    async with AsyncSessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        finally:
            await db.close()


# Определяем URL базы данных в зависимости от режима
DATABASE_URL_SYNC = f"postgresql+psycopg2://{url}"

# Синхронный движок
engine = create_engine(DATABASE_URL_SYNC, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=Session, autocommit=False, autoflush=False)


# Генератор сессии для FastAPI Depends
def sync_get_db():
    """Синхронный движок"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
