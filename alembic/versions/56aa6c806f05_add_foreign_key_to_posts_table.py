import sqlmodel

"""add foreign key to posts table

Revision ID: 56aa6c806f05
Revises: d93dd59b26ec
Create Date: 2025-03-08 01:12:27.429361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56aa6c806f05'
down_revision: Union[str, None] = 'd93dd59b26ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', 'posts', 'users', ['owner_id'], ['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("posts_users_fk", "posts")
    op.drop_column("posts", column_name="owner_id")
    pass
