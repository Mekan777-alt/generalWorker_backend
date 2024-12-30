"""add CASCADE delete to tasks and all model

Revision ID: 16a37bf38526
Revises: 339a93c24f86
Create Date: 2024-12-30 18:08:45.502128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16a37bf38526'
down_revision: Union[str, None] = '339a93c24f86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('reviews_executor_id_fkey', 'reviews', type_='foreignkey')
    op.drop_constraint('reviews_customer_id_fkey', 'reviews', type_='foreignkey')
    op.create_foreign_key(None, 'reviews', 'executor_profile', ['executor_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'reviews', 'customer_profile', ['customer_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('tasks_customer_id_fkey', 'tasks', type_='foreignkey')
    op.create_foreign_key(None, 'tasks', 'customer_profile', ['customer_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.create_foreign_key('tasks_customer_id_fkey', 'tasks', 'customer_profile', ['customer_id'], ['id'])
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.create_foreign_key('reviews_customer_id_fkey', 'reviews', 'customer_profile', ['customer_id'], ['id'])
    op.create_foreign_key('reviews_executor_id_fkey', 'reviews', 'executor_profile', ['executor_id'], ['id'])
    # ### end Alembic commands ###
