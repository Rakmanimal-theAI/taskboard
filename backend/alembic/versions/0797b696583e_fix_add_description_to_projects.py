"""fix add description to projects

Revision ID: 0797b696583e
Revises: 172f24e3daad
Create Date: 2026-05-24 12:59:57.435256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0797b696583e'
down_revision: Union[str, Sequence[str], None] = '172f24e3daad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('projects', sa.Column('description', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('projects', 'description')
