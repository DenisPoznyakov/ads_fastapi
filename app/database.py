import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.models import Base

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "padzzzer18flot18vk")
DB_NAME = os.getenv("POSTGRES_DB", "adsdb")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def wait_for_postgres():
    """Ждём, пока база станет доступной"""
    max_attempts = 20
    for i in range(max_attempts):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            print("PostgreSQL готова!")
            return
        except Exception as e:
            print(f"Ожидание базы... ({i+1}/{max_attempts})", e)
            await asyncio.sleep(2)
    raise TimeoutError("Не удалось подключиться к PostgreSQL за отведённое время")


async def init_db():
    """БЕЗОПАСНО создаём таблицы — сначала ждём, пока БД будет готова"""
    await wait_for_postgres()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы созданы / уже существуют")