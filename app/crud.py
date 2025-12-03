from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app import models

# Создание объявления
async def create_ad(session: AsyncSession, ad_data: dict):
    ad = models.Ad(**ad_data)
    session.add(ad)
    await session.commit()
    await session.refresh(ad)
    return ad

# Получение объявления по id
async def get_ad(session: AsyncSession, ad_id: int):
    return await session.get(models.Ad, ad_id)

# Получение списка объявлений с лимитом и оффсетом
async def list_ads(session: AsyncSession, limit: int = 50, offset: int = 0):
    result = await session.execute(select(models.Ad).limit(limit).offset(offset))
    return result.scalars().all()

# Обновление объявления
async def update_ad(session: AsyncSession, ad_id: int, ad_data: dict):
    ad = await session.get(models.Ad, ad_id)
    if not ad:
        return None
    for key, value in ad_data.items():
        if hasattr(ad, key):
            setattr(ad, key, value)
    session.add(ad)
    await session.commit()
    await session.refresh(ad)
    return ad

# Удаление объявления
async def delete_ad(session: AsyncSession, ad_id: int):
    ad = await session.get(models.Ad, ad_id)
    if not ad:
        return None
    await session.delete(ad)
    await session.commit()
    return ad
