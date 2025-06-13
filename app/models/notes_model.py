from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Notes(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    creator = relationship("User", back_populates="notes")
