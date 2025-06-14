"""Remove conflicting labels column from notes

Revision ID: fb9783632e72
Revises: cafce3bf7676
Create Date: 2025-06-14 14:30:50.754562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb9783632e72'
down_revision: Union[str, None] = 'cafce3bf7676'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('notes', 'labels')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('notes', sa.Column('labels', sa.VARCHAR(), nullable=True))
