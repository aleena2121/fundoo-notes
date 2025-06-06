from datetime import date, datetime
from app.database import Base
from sqlalchemy.dialects.postgresql import ENUM as SQLEnum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from . import enum
    

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] 
    username: Mapped[str]
    password: Mapped[str]
    dob: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    gender: Mapped[enum.GenderEnum] = mapped_column(SQLEnum(enum.GenderEnum, name="gender_enum"))
