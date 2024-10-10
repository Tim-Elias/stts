"""Добавить уникальный индекс для use_automatic

Revision ID: 7ed55c76ec3a
Revises: bea33fbb4d37
Create Date: 2024-10-09 14:38:18.839123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ed55c76ec3a'
down_revision: Union[str, None] = 'bea33fbb4d37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем уникальный индекс для столбца use_automatic,
    # чтобы только один ряд мог быть True
    op.create_index('uq_prompts_use_automatic', 'prompts', ['use_automatic'], unique=True, postgresql_where=sa.text('use_automatic IS TRUE'))


def downgrade() -> None:
    # Удаляем уникальный индекс
    op.drop_index('uq_prompts_use_automatic', 'prompts')
