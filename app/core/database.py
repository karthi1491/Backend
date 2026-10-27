from pymongo import AsyncMongoClient

from app.core.config import settings


client = AsyncMongoClient(settings.MONGODB_URI)

db = client[settings.MONGODB_DB]


async def connect_db():
    await client.admin.command("ping")
    print("MongoDB connected successfully")


async def close_db():
    await client.close()
    print("MongoDB connection closed")