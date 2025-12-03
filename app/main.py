from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from app import models, schemas, crud, database
import asyncio

# Создаем базу, если еще не создана
async def init_db():
    async with database.engine.begin() as conn:
        # Импортируем модели и создаем таблицы
        await conn.run_sync(models.Base.metadata.create_all)

# Создаем приложение
app = FastAPI(title="Ads API")

# Роуты
@app.on_event("startup")
async def on_startup():
    # Инициализация БД при старте
    await init_db()
    print("Database initialized")

# Создание объявления
@app.post("/advertisement", response_model=schemas.AdSchema)
async def create_ad_endpoint(ad: schemas.AdCreate):
    async with database.AsyncSessionLocal() as session:
        return await crud.create_ad(session, ad.dict())

# Получение объявления по id
@app.get("/advertisement/{ad_id}", response_model=schemas.AdSchema)
async def get_ad_endpoint(ad_id: int):
    async with database.AsyncSessionLocal() as session:
        ad = await crud.get_ad(session, ad_id)
        if not ad:
            raise HTTPException(status_code=404, detail="Ad not found")
        return ad

# Получение списка объявлений с фильтром по автору и лимитом
@app.get("/advertisement", response_model=List[schemas.AdSchema])
async def list_ads_endpoint(
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    owner: Optional[str] = None
):
    async with database.AsyncSessionLocal() as session:
        ads = await crud.list_ads(session, limit=limit, offset=offset)
        if owner:
            ads = [ad for ad in ads if ad.owner == owner]
        return ads

# Обновление объявления
@app.patch("/advertisement/{ad_id}", response_model=schemas.AdSchema)
async def update_ad_endpoint(ad_id: int, ad: schemas.AdCreate):
    async with database.AsyncSessionLocal() as session:
        updated_ad = await crud.update_ad(session, ad_id, ad.dict(exclude_unset=True))
        if not updated_ad:
            raise HTTPException(status_code=404, detail="Ad not found")
        return updated_ad

# Удаление объявления
@app.delete("/advertisement/{ad_id}")
async def delete_ad_endpoint(ad_id: int):
    async with database.AsyncSessionLocal() as session:
        deleted_ad = await crud.delete_ad(session, ad_id)
        if not deleted_ad:
            raise HTTPException(status_code=404, detail="Ad not found")
        return {"status": "deleted"}
