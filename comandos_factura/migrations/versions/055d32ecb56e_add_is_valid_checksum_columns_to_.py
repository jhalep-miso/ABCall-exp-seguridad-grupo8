"""add is_valid_checksum columns to factura_audits

Revision ID: 055d32ecb56e
Revises: 8e9a2602fa8f
Create Date: 2024-09-29 00:00:57.975029

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '055d32ecb56e'
down_revision = '8e9a2602fa8f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'factura_audits',
        sa.Column(
            'is_valid_checksum', sa.Boolean(), nullable=False, server_default='false'
        ),
    )


def downgrade():
    op.drop_column('factura_audits', 'is_valid_checksum')
