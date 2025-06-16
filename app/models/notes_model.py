# from datetime import datetime, timedelta, timezone
# from typing import TYPE_CHECKING, List

# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from app.models.association import note_label_association
# from app.database import Base
# from .labels_model import Labels
# class Notes(Base):
#     __tablename__ = "notes"
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     title: Mapped[str]
#     content: Mapped[str]
#     created_at: Mapped[datetime] = mapped_column(
#         default=lambda: datetime.now(timezone.utc)
#     )
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     expiry_date: Mapped[datetime] = mapped_column(
#         default=lambda: datetime.now(timezone.utc) + timedelta(weeks=1)
#     )

#     labels: Mapped[List[Labels]] = relationship(
#         "Labels", secondary=note_label_association, back_populates="notes"
#     )

#     creator: Mapped["User"] = relationship("User", back_populates="notes")



from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.association import note_label_association

if TYPE_CHECKING:
    from app.models.labels_model import Labels
    from app.models.user_model import User

class Notes(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expiry_date: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc) + timedelta(weeks=1)
    )

    # Use string reference for Labels
    labels: Mapped[List["Labels"]] = relationship(
        "Labels", secondary=note_label_association, back_populates="notes"
    )

    # Corrected string reference for User
    creator: Mapped["User"] = relationship("User", back_populates="notes")
