from app.core.database import db


COLLECTION = db["profiles"]
PROFILE_ID = "primary"


async def create_profile(data: dict):
    await COLLECTION.insert_one({
        "_id": PROFILE_ID,
        **data,
    })


async def get_profile():
    return await COLLECTION.find_one(
        {"_id": PROFILE_ID},
        {"_id": 0},
    )


async def update_profile(data: dict):
    result = await COLLECTION.update_one(
        {"_id": PROFILE_ID},
        {"$set": data},
    )

    return result.matched_count > 0