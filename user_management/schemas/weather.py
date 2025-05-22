from pydantic import BaseModel

class WeatherBase(BaseModel):
    city: str
    temperature: float
    humidity: int
    description: str

class WeatherCreate(WeatherBase):
    pass

class WeatherResponse(WeatherBase):
    id: int

    class Config:
        orm_mode = True