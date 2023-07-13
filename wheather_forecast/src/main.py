from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests
from datetime import datetime, timedelta

app = FastAPI()

class WeatherData(BaseModel):
    lat: float
    lon: float
    detailing_type: str

class WeatherForecast(BaseModel):
    timestamp: int
    temperature: float
    humidity: float

weather_data_cache = {}

def fetch_weather_data(lat: float, lon: float, detailing_type: str):
    # Make a request to OpenWeatherMap API
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily&appid={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data")
    return response.json()
