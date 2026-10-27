from pydantic import BaseModel
from datetime import datetime


class ResumeResponse(BaseModel):
    filename: str
    content: str
    uploaded_at: datetime