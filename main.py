# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select

from models import FarmProfile
from database import database, farms, users
from crud import create_user, get_user
from weather import get_weather_data

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()

@app.post("/create_farm_profile")
async def create_farm_profile(farm: FarmProfile):
    query = farms.insert().values(location=farm.location, crops=farm.crops)
    farm_id = await database.execute(query)
    return {"id": farm_id, **farm.dict()}

@app.get("/get_farm_profile/{farm_id}")
async def get_farm_profile(farm_id: int):
    query = farms.select().where(farms.c.id == farm_id)
    farm = await database.fetch_one(query)
    if farm is None:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/create_user")
async def create_user_endpoint(username: str, email: str, farm_id: int):
    return await create_user(username, email, farm_id)

@app.get("/get_user/{user_id}")
async def get_user_endpoint(user_id: int):
    user = await get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/get_weather/{city}")
async def get_weather(city: str):
    api_key = "openweathermap_api_key"
    weather_data = await get_weather_data(api_key, city)
    return weather_data

@app.post("/generate_crop_recommendations")
async def generate_crop_recommendations(user_id: int, city: str):
    pass

@app.post("/send_notification")
async def send_notification(user_id: int, message: str):
    pass