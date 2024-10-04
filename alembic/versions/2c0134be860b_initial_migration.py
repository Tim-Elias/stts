"""Initial migration

Revision ID: 2c0134be860b
Revises: 
Create Date: 2024-10-04 14:18:40.786527

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Float, Text, DateTime
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '2c0134be860b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем таблицу users (включая новые поля)
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String, nullable=True),
        sa.Column('user_id', sa.String, unique=True, nullable=False),
        sa.Column('password_hash', sa.String, nullable=True),
        sa.Column('google_id', sa.String, unique=True, nullable=True),
        sa.Column('auth_type', sa.String, nullable=False, default='password'),
        sa.Column('user_type', sa.String, default='user')
    )

    # Создаем таблицу audio_files
    op.create_table(
        'audio_files',
        sa.Column('audio_id', sa.String, primary_key=True),
        sa.Column('user', sa.String(255), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('file_extension', sa.String(255), nullable=False),
        sa.Column('file_size', sa.Float, nullable=False),
        sa.Column('upload_date', sa.DateTime, default=datetime.utcnow),
        sa.Column('bucket_name', sa.String(255), nullable=False),
        sa.Column('s3_key', sa.String(255), nullable=False)
    )

    # Создаем таблицу prompts
    op.create_table(
        'prompts',
        sa.Column('prompt_id', sa.String, primary_key=True),
        sa.Column('user', sa.String(255), nullable=False),
        sa.Column('prompt_name', sa.String(255), nullable=False),
        sa.Column('text', sa.Text)
    )

    # Создаем таблицу transcriptions
    op.create_table(
        'transcriptions',
        sa.Column('transcription_id', sa.String, primary_key=True),
        sa.Column('user', sa.String(255), nullable=False),
        sa.Column('audio_id', sa.String(255), nullable=False),
        sa.Column('text', sa.Text),
        sa.Column('analysis', sa.Text),
        sa.Column('prompt', sa.Text),
        sa.Column('tokens', sa.Integer)
    )


def downgrade() -> None:
    # Удаляем таблицу transcriptions
    op.drop_table('transcriptions')

    # Удаляем таблицу prompts
    op.drop_table('prompts')

    # Удаляем таблицу audio_files
    op.drop_table('audio_files')

    # Удаляем таблицу users
    op.drop_table('users')
