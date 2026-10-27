from datetime import datetime, timezone
from uuid import uuid4

from app.core.database import get_database


async def save_optimization(
    job_description: str,
    suggestions: list[dict],
    missing_skills: list[str],
    summary: str,
    resume_text: str,
):
    db = get_database()

    optimization_id = str(uuid4())

    document = {
        "_id": optimization_id,
        "status": "pending",
        "job_description": job_description,
        "original_resume_text": resume_text,
        "suggestions": [
            {
                **suggestion,
                "suggestion_id": str(uuid4()),
                "decision": "pending",
            }
            for suggestion in suggestions
        ],
        "missing_skills": missing_skills,
        "summary": summary,
        "created_at": datetime.now(timezone.utc),
    }

    await db["resume_optimizations"].insert_one(document)

    return document


async def get_optimization(optimization_id: str):
    db = get_database()

    return await db["resume_optimizations"].find_one(
        {"_id": optimization_id}
    )



async def update_optimization_review(
    optimization_id: str,
    decisions: dict[str, str],
):
    db = get_database()  # Use your existing working DB accessor.

    optimization = await get_optimization(optimization_id)

    if optimization is None:
        return None

    if optimization["status"] != "pending":
        raise ValueError("Optimization has already been reviewed")

    for suggestion in optimization["suggestions"]:
        suggestion_id = suggestion["suggestion_id"]

        suggestion["decision"] = decisions[suggestion_id]

    optimization["status"] = "reviewed"
    optimization["reviewed_at"] = datetime.now(timezone.utc)

    result = await db["resume_optimizations"].update_one(
        {
            "_id": optimization_id,
            "status": "pending",
        },
        {
            "$set": {
                "suggestions": optimization["suggestions"],
                "status": "reviewed",
                "reviewed_at": optimization["reviewed_at"],
            }
        },
    )

    if result.modified_count == 0:
        raise ValueError("Optimization was already reviewed")

    return optimization




async def update_optimization_review(
    optimization_id: str,
    decisions: dict[str, str],
):
    db = get_database()  # Reuse your working database accessor.

    optimization = await get_optimization(optimization_id)

    if optimization is None:
        return None

    if optimization["status"] != "pending":
        raise ValueError("Optimization already reviewed")

    updated_suggestions = []

    for suggestion in optimization["suggestions"]:
        updated_suggestions.append({
            **suggestion,
            "decision": decisions[suggestion["suggestion_id"]],
        })

    reviewed_at = datetime.now(timezone.utc)

    result = await db["resume_optimizations"].update_one(
        {
            "_id": optimization_id,
            "status": "pending",
        },
        {
            "$set": {
                "suggestions": updated_suggestions,
                "status": "reviewed",
                "reviewed_at": reviewed_at,
            }
        },
    )

    if result.modified_count == 0:
        raise ValueError("Optimization already reviewed")

    return {
        **optimization,
        "suggestions": updated_suggestions,
        "status": "reviewed",
        "reviewed_at": reviewed_at,
    }