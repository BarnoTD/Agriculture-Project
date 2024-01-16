from sqlalchemy import select
from database import database, users

async def create_user(username: str, email: str, farm_id: int):
    query = users.insert().values(username=username, email=email, farm_id=farm_id)
    user_id = await database.execute(query)
    return {"id": user_id, "username": username, "email": email, "farm_id": farm_id}

async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)
