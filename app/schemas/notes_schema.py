from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Notes(BaseModel):
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class UpdateNote(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
