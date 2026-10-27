from app.core.database import db

COLLECTION = db["resumes"]


async def save_resume(data: dict):
    await COLLECTION.replace_one(
        {"_id": "primary"},
        {"_id": "primary", **data},
        upsert=True,
    )


async def get_resume():
    return await COLLECTION.find_one(
        {"_id": "primary"},
        {"_id": 0},
    )