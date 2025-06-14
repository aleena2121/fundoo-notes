from datetime import date, datetime
from typing import List, Optional

from sqlalchemy.dialects.postgresql import ENUM as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from . import enum


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    dob: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    gender: Mapped[enum.GenderEnum] = mapped_column(
        SQLEnum(enum.GenderEnum, name="gender_enum")
    )
    secret_key: Mapped[str]
    is_verified: Mapped[bool] = mapped_column(default=False)

    notes: Mapped[List["Notes"]] = relationship(
        "Notes", 
        back_populates="creator",
        cascade="all, delete-orphan" 
    )
    labels: Mapped[List["Labels"]] = relationship(
        "Labels", 
        back_populates="creator",
        cascade="all, delete-orphan"  
    )