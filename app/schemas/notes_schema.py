from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class LabelResponse(BaseModel):
    id: int
    title: str
    
    class Config:
        from_attributes = True

class Notes(BaseModel):
    title: str
    content: str
    labels: List[str]
    created_at: datetime

    class Config:
        from_attributes = True

class NotesResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    user_id: int
    labels: List[LabelResponse] = []  
    
    class Config:
        from_attributes = True

class UpdateNote(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    labels : Optional[List[str]] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
