"""fix tasks columns

Revision ID: 8438ceab8f59
Revises: 22958947cfb7
Create Date: 2026-05-24 13:03:37.101811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8438ceab8f59'
down_revision: Union[str, Sequence[str], None] = '22958947cfb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('tasks', 'assignee_id', nullable=True)
    op.alter_column('tasks', 'due_date', nullable=True)
    op.add_column('tasks', sa.Column('created_at', sa.DateTime(), nullable=True))

def downgrade():
    op.alter_column('tasks', 'assignee_id', nullable=False)
    op.alter_column('tasks', 'due_date', nullable=False)
    op.drop_column('tasks', 'created_at')
