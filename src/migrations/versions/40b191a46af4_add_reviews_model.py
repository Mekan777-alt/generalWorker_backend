"""add reviews model

Revision ID: 40b191a46af4
Revises: e086d9bc7069
Create Date: 2024-11-17 21:14:13.404612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40b191a46af4'
down_revision: Union[str, None] = 'e086d9bc7069'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('executor_id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Boolean(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customer_profile.id'], ),
    sa.ForeignKeyConstraint(['executor_id'], ['executor_profile.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user_roles_rating')
    op.add_column('task_responses', sa.Column('text', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task_responses', 'text')
    op.create_table('user_roles_rating',
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('plus', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('minus', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='user_roles_rating_role_id_fkey'),
    sa.PrimaryKeyConstraint('role_id', name='user_roles_rating_pkey')
    )
    op.drop_table('reviews')
    # ### end Alembic commands ###