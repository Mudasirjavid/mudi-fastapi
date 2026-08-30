"""add content column to posts table

Revision ID: a49e104bd6a1
Revises: 2c33b429d766
Create Date: 2026-08-30 14:39:24.683165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a49e104bd6a1'
down_revision: Union[str, Sequence[str], None] = '2c33b429d766'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
