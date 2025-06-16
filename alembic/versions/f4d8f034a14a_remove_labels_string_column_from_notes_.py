"""Remove labels string column from notes table

Revision ID: f4d8f034a14a
Revises: 038bf859fc2a
Create Date: 2025-06-14 12:46:19.782824

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f4d8f034a14a"
down_revision: Union[str, None] = "038bf859fc2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("notes", "labels")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("notes", sa.Column("labels", sa.String(), nullable=True))
