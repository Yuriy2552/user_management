from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from user_management.dependencies import get_db
from user_management.models.weather import Weather
from user_management.schemas.weather import WeatherCreate, WeatherResponse

router = APIRouter()

@router.post("/", response_model=WeatherResponse, summary="Добавить данные о погоде")
async def create_weather(weather: WeatherCreate, db: AsyncSession = Depends(get_db)):
    new_weather = Weather(**weather.dict())
    db.add(new_weather)
    await db.commit()
    await db.refresh(new_weather)
    return new_weather

@router.get("/{city}", response_model=WeatherResponse, summary="Получить данные о погоде по городу")
async def get_weather(city: str, db: AsyncSession = Depends(get_db)):
    query = select(Weather).filter(Weather.city == city)
    result = await db.execute(query)
    weather = result.scalars().first()
    if not weather:
        raise HTTPException(status_code=404, detail="Данные о погоде не найдены")
    return weather