"""fix add created_at to projects

Revision ID: 22958947cfb7
Revises: 0797b696583e
Create Date: 2026-05-24 13:02:07.032072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22958947cfb7'
down_revision: Union[str, Sequence[str], None] = '0797b696583e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('projects', sa.Column('created_at', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('projects', 'created_at')
