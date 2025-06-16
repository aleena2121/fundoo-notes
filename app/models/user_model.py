# from datetime import date, datetime
# from typing import TYPE_CHECKING, List, Optional

# from sqlalchemy.dialects.postgresql import ENUM as SQLEnum
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.database import Base

# from ..utils import enum

# if TYPE_CHECKING:
#     from app.models.notes_model import Notes
#     from app.models.labels_model import Labels
# class User(Base):
#     __tablename__ = "users"
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     name: Mapped[str]
#     username: Mapped[str]
#     password: Mapped[str]
#     dob: Mapped[date]
#     created_at: Mapped[datetime] = mapped_column(default=datetime.now)
#     gender: Mapped[enum.GenderEnum] = mapped_column(
#         SQLEnum(enum.GenderEnum, name="gender_enum")
#     )
#     secret_key: Mapped[str]
#     is_verified: Mapped[bool] = mapped_column(default=False)

#     # notes: Mapped[List["Notes"]] = relationship(
#     #     "Notes", back_populates="creator", cascade="all, delete-orphan"
#     # )
#     # labels: Mapped[List["Labels"]] = relationship(
#     #     "Labels", back_populates="creator", cascade="all, delete-orphan"
#     # )


#     notes: Mapped[List["Notes"]] = relationship("Notes", back_populates="creator")
#     labels: Mapped[List["Labels"]] = relationship("Labels", back_populates="creator")


from datetime import date, datetime
from typing import TYPE_CHECKING, List

from sqlalchemy.dialects.postgresql import ENUM as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from ..utils import enum

if TYPE_CHECKING:
    from app.models.notes_model import Notes
    from app.models.labels_model import Labels


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
        "Notes", back_populates="creator", cascade="all, delete-orphan"
    )
    labels: Mapped[List["Labels"]] = relationship(
        "Labels", back_populates="creator", cascade="all, delete-orphan"
    )
