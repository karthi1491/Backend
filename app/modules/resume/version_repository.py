from datetime import datetime, timezone
from uuid import uuid4

# Import your existing working database accessor.
from app.core.database import get_database


async def save_resume_version(
    optimization_id: str,
    resume_text: str,
):
    db = get_database()

    version_id = str(uuid4())

    document = {
        "_id": version_id,
        "optimization_id": optimization_id,
        "resume_text": resume_text,
        "created_at": datetime.now(timezone.utc),
    }

    await db["resume_versions"].insert_one(document)

    return document


async def get_resume_version(version_id: str):
    db = get_database()

    return await db["resume_versions"].find_one(
        {"_id": version_id}
    )