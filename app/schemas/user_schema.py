from datetime import date
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
