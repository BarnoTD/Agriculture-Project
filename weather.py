import httpx

async def get_weather_data(api_key: str, city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()