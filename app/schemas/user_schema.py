from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.models.enum import GenderEnum


class User(BaseModel):
    name: str
    username: str
    password: str
    dob: date
    gender: GenderEnum

    class Config:
        from_attributes = True


class ShowUser(BaseModel):
    name: str
    username: str
    dob: date
    gender: GenderEnum


class UpdateUser(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[GenderEnum] = None
