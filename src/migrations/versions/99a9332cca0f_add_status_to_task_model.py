"""add status to task model

Revision ID: 99a9332cca0f
Revises: e7622ab5870f
Create Date: 2024-11-13 17:23:25.253237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99a9332cca0f'
down_revision: Union[str, None] = 'e7622ab5870f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем перечисление для PostgreSQL
    tasks_status_enum = sa.Enum('CREATED', 'PROCESSING', 'COMPLETED', 'CANCELLED', name='tasksstatusenum')
    tasks_status_enum.create(op.get_bind(), checkfirst=True)

    # Добавляем колонку статуса с новым типом
    op.add_column('tasks', sa.Column('status', tasks_status_enum, nullable=True))


def downgrade() -> None:
    # Удаляем колонку статуса
    op.drop_column('tasks', 'status')

    # Удаляем тип перечисления
    tasks_status_enum = sa.Enum('CREATED', 'PROCESSING', 'COMPLETED', 'CANCELLED', name='tasksstatusenum')
    tasks_status_enum.drop(op.get_bind(), checkfirst=True)
