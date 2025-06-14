from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.association import note_label_association
from app.models.notes_model import Notes


class Labels(Base):
    __tablename__ = "labels"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    creator: Mapped["User"] = relationship("User", back_populates="labels")
    notes: Mapped[List["Notes"]] = relationship(
        "Notes", 
        secondary=note_label_association, 
        back_populates="labels"
    )
