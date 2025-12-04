from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import async_session, init_db
from app.schemas import AdCreate, AdUpdate, AdResponse
from app import crud


app = FastAPI(
    title="Advertisements API",
    description="Простое API для объявлений (учебный проект Netology)",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event() -> None:
    """Выполняется один раз при старте приложения"""
    print("Запуск приложения... Ожидание подключения к базе данных")
    await init_db()
    print("Приложение успешно запущено и готово к работе!")


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


# ──────────────────────────────────────────────────────────────
# Эндпоинты
# ──────────────────────────────────────────────────────────────

@app.post("/advertisement", response_model=AdResponse, status_code=201)
async def create_ad(ad: AdCreate, session: AsyncSession = Depends(get_session)):
    return await crud.create_ad(session=session, ad_in=ad)


@app.get("/advertisement/{ad_id}", response_model=AdResponse)
async def get_ad(ad_id: int, session: AsyncSession = Depends(get_session)):
    ad = await crud.get_ad(session=session, ad_id=ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad


@app.patch("/advertisement/{ad_id}", response_model=AdResponse)
async def update_ad(
    ad_id: int,
    ad_update: AdUpdate,
    session: AsyncSession = Depends(get_session)
):
    ad = await crud.update_ad(session=session, ad_id=ad_id, ad_in=ad_update)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad


@app.delete("/advertisement/{ad_id}", status_code=200)
async def delete_ad(ad_id: int, session: AsyncSession = Depends(get_session)):
    success = await crud.delete_ad(session=session, ad_id=ad_id)
    if not success:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return {"message": "Advertisement successfully deleted"}


@app.get("/advertisement", response_model=List[AdResponse])
async def search_ads(
    title: str | None = Query(None, description="Поиск по заголовку (частичное совпадение)"),
    description: str | None = Query(None, description="Поиск по описанию"),
    owner: str | None = Query(None, description="Фильтр по владельцу"),
    price_min: float | None = Query(None, ge=0, description="Минимальная цена"),
    price_max: float | None = Query(None, ge=0, description="Максимальная цена"),
    session: AsyncSession = Depends(get_session),
):
    return await crud.search_ads(
        session=session,
        title=title,
        description=description,
        owner=owner,
        price_min=price_min,
        price_max=price_max,
    )


@app.get("/")
async def root():
    return {
        "message": "Advertisements API работает!",
        "docs": "/docs",
        "redoc": "/redoc"
    }