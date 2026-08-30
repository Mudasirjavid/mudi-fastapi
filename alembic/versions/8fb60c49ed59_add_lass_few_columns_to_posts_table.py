"""add lass few columns to posts table

Revision ID: 8fb60c49ed59
Revises: 12537be2d02c
Create Date: 2026-08-30 15:35:41.187704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fb60c49ed59'
down_revision: Union[str, Sequence[str], None] = '12537be2d02c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
    'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
    'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text
    ('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
