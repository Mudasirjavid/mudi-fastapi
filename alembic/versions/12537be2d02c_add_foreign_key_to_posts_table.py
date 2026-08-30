"""add foreign-key to posts table

Revision ID: 12537be2d02c
Revises: c024dc72ce5e
Create Date: 2026-08-30 15:19:30.762906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12537be2d02c'
down_revision: Union[str, Sequence[str], None] = 'c024dc72ce5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")

pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
