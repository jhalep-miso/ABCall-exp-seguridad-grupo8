"""agregar columna de checksum a facturas

Revision ID: 8e9a2602fa8f
Revises: b7e9450d06e0
Create Date: 2024-09-28 15:57:41.032235

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e9a2602fa8f'
down_revision = 'b7e9450d06e0'
branch_labels = None
depends_on = None


def upgrade():
    # add checksum column to facturas table
    op.add_column(
        'facturas',
        sa.Column('checksum', sa.String(64), nullable=False, server_default=''),
    )


def downgrade():
    # remove checksum column from facturas table
    op.drop_column('facturas', 'checksum')
