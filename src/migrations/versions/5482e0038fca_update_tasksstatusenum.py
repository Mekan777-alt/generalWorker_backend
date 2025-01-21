"""Update TasksStatusEnum

Revision ID: 5482e0038fca
Revises: d1cde348ea29
Create Date: 2025-01-21 11:35:58.412354

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '5482e0038fca'
down_revision: Union[str, None] = 'd1cde348ea29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Название enum-типа в базе данных
ENUM_NAME = "tasksstatusenum"


def upgrade() -> None:
    # Добавляем новые значения в ENUM
    op.execute(f"ALTER TYPE {ENUM_NAME} ADD VALUE 'UNDER_REVIEW'")


def downgrade() -> None:
    # Откат изменений: пересоздаем ENUM без новых значений
    op.execute(f"CREATE TYPE {ENUM_NAME}_old AS ENUM('SEARCH', 'WORK', 'COMPLETED')")
    op.execute(f"ALTER TABLE tasks ALTER COLUMN status TYPE {ENUM_NAME}_old USING status::text::{ENUM_NAME}_old")
    op.execute(f"DROP TYPE {ENUM_NAME}")
    op.execute(f"ALTER TYPE {ENUM_NAME}_old RENAME TO {ENUM_NAME}")