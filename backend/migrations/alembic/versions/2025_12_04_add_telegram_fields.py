"""add telegram fields to companies

Revision ID: add_telegram_fields
Revises: add_updated_at_to_users
Create Date: 2025-12-04

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_telegram_fields'
down_revision: Union[str, None] = '89fdd5826091'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('companies', sa.Column('telegram_bot_token', sa.String(), nullable=True))
    op.add_column('companies', sa.Column('telegram_chat_id', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('companies', 'telegram_chat_id')
    op.drop_column('companies', 'telegram_bot_token')

