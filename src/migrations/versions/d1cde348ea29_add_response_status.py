"""add response status

Revision ID: d1cde348ea29
Revises: 1b1a4e959bb2
Create Date: 2025-01-19 18:23:27.421044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1cde348ea29'
down_revision: Union[str, None] = '1b1a4e959bb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем тип ENUM responsestatus
    responsestatus_enum = sa.Enum('REJECTED', 'ACCEPTED', 'EXPECTATION', name='responsestatus')
    responsestatus_enum.create(op.get_bind())  # Создаем тип в базе данных

    # Добавляем колонку status с типом responsestatus
    op.add_column(
        'task_responses',
        sa.Column('status', responsestatus_enum, nullable=True)
    )


def downgrade() -> None:
    # Удаляем колонку status
    op.drop_column('task_responses', 'status')

    # Удаляем тип ENUM responsestatus
    responsestatus_enum = sa.Enum('REJECTED', 'ACCEPTED', 'EXPECTATION', name='responsestatus')
    responsestatus_enum.drop(op.get_bind())
