from sqlalchemy import Column, ForeignKey, Table
from app.database import Base

note_label_association = Table(
    "note_label_association",
    Base.metadata,
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
    Column("label_id", ForeignKey("labels.id"), primary_key=True),
)
