"""add a column

Revision ID: 84cdd9bb8fce
Revises: 2b56acf7a7fe
Create Date: 2024-03-07 16:37:28.107154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84cdd9bb8fce'
down_revision: Union[str, None] = '2b56acf7a7fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))

def downgrade():
    op.drop_column('account', 'last_transaction_date')
