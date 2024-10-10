"""Добавить булевый столбец use_automatic в таблицу prompts

Revision ID: bea33fbb4d37
Revises: 2c0134be860b
Create Date: 2024-10-09 14:18:03.172719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bea33fbb4d37'
down_revision: Union[str, None] = '2c0134be860b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем новый булевый столбец use_automatic в таблицу prompts
    op.add_column('prompts', sa.Column('use_automatic', sa.Boolean(), nullable=True))


def downgrade() -> None:
    # Удаляем добавленный булевый столбец use_automatic из таблицы prompts
    op.drop_column('prompts', 'use_automatic')
