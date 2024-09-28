"""crear tabla facturas

Revision ID: 6a9b289d8a7e
Revises: 
Create Date: 2024-09-27 01:30:14.677851

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a9b289d8a7e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'facturas',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('usuario_id', sa.Integer, nullable=False),
        sa.Column('nombre', sa.String(128), nullable=False),
        sa.Column('monto', sa.Float, nullable=False),
        sa.Column('detalle', sa.String(128), nullable=False),
        sa.Column('estado', sa.String(128), nullable=False),
        sa.Column('fecha', sa.DateTime, nullable=False),
    )


def downgrade():
    op.drop_table('facturas')
