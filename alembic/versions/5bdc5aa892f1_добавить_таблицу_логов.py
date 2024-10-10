"""Добавить таблицу логов

Revision ID: 5bdc5aa892f1
Revises: 7ed55c76ec3a
Create Date: 2024-10-10 15:39:58.051301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5bdc5aa892f1'
down_revision: Union[str, None] = '7ed55c76ec3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем таблицу logs
    op.create_table(
        'logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=False),  # ID пользователя
        sa.Column('action', sa.String(length=255), nullable=False),    # Действие
        sa.Column('message', sa.String(length=255), nullable=False),   # Сообщение
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.func.now()),  # Время
        sa.PrimaryKeyConstraint('id')  # Установка первичного ключа
    )


def downgrade() -> None:
    # Удаляем таблицу logs
    op.drop_table('logs')
