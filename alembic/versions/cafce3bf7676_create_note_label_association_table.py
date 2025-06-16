"""Create note_label_association table

Revision ID: cafce3bf7676
Revises: f4d8f034a14a
Create Date: 2025-06-14 12:47:07.590723

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cafce3bf7676"
down_revision: Union[str, None] = "f4d8f034a14a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "note_label_association",
        sa.Column("note_id", sa.Integer(), nullable=False),
        sa.Column("label_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["label_id"],
            ["labels.id"],
        ),
        sa.ForeignKeyConstraint(
            ["note_id"],
            ["notes.id"],
        ),
        sa.PrimaryKeyConstraint("note_id", "label_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("note_label_association")
