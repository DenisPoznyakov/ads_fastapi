import asyncio
from app import models, database

async def init_db():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    print("Tables created")

asyncio.run(init_db())
