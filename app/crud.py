from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Advertisement
from app.schemas import AdCreate, AdUpdate

async def create_ad(session: AsyncSession, ad: AdCreate) -> Advertisement:
    new_ad = Advertisement(**ad.model_dump())
    session.add(new_ad)
    await session.commit()
    await session.refresh(new_ad)
    return new_ad

async def get_ad(session: AsyncSession, ad_id: int) -> Advertisement | None:
    result = await session.execute(select(Advertisement).where(Advertisement.id == ad_id))
    return result.scalars().first()

async def update_ad(session: AsyncSession, ad_id: int, ad_update: AdUpdate) -> Advertisement | None:
    ad = await get_ad(session, ad_id)
    if not ad:
        return None
    for key, value in ad_update.model_dump(exclude_unset=True).items():
        setattr(ad, key, value)
    session.add(ad)
    await session.commit()
    await session.refresh(ad)
    return ad

async def delete_ad(session: AsyncSession, ad_id: int) -> bool:
    ad = await get_ad(session, ad_id)
    if not ad:
        return False
    await session.delete(ad)
    await session.commit()
    return True

async def search_ads(session: AsyncSession, title: str | None = None, description: str | None = None,
                     owner: str | None = None, price_min: float | None = None, price_max: float | None = None):
    query = select(Advertisement)
    filters = []
    if title:
        filters.append(Advertisement.title.ilike(f"%{title}%"))
    if description:
        filters.append(Advertisement.description.ilike(f"%{description}%"))
    if owner:
        filters.append(Advertisement.owner == owner)
    if price_min is not None:
        filters.append(Advertisement.price >= price_min)
    if price_max is not None:
        filters.append(Advertisement.price <= price_max)
    if filters:
        query = query.where(and_(*filters))
    result = await session.execute(query)
    return result.scalars().all()
