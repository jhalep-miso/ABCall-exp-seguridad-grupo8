"""add factura_id column to factura_audits

Revision ID: 461069cba2aa
Revises: 055d32ecb56e
Create Date: 2024-09-29 01:15:50.070346

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '461069cba2aa'
down_revision = '055d32ecb56e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'factura_audits',
        sa.Column('factura_id', sa.Integer(), nullable=True),
    )

    # actualizar la función del trigger para incluir factura_id en factura_audits
    op.execute(
        """
        CREATE OR REPLACE FUNCTION before_update_facturas()
        RETURNS TRIGGER AS $$
        DECLARE
            db_user TEXT;
            db_user_ip TEXT;
            execution_time TIMESTAMP;
        BEGIN
            select inet_client_addr() into db_user_ip;
            select session_user into db_user;
            execution_time := now();

            RAISE NOTICE 'DB User %, with IP %, is updating factura_id %', db_user, db_user_ip, OLD.id;

            INSERT INTO factura_audits (factura_id, old_data, new_data, db_user, db_user_ip, execution_time)
            VALUES (OLD.id, row_to_json(OLD), row_to_json(NEW), db_user, db_user_ip, execution_time);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )



def downgrade():
    op.drop_column('factura_audits', 'factura_id')

    op.execute(
        """
        CREATE OR REPLACE FUNCTION before_update_facturas()
        RETURNS TRIGGER AS $$
        DECLARE
            db_user TEXT;
            db_user_ip TEXT;
            execution_time TIMESTAMP;
        BEGIN
            select inet_client_addr() into db_user_ip;
            select session_user into db_user;
            execution_time := now();

            RAISE NOTICE 'DB User %, with IP %, is updating row in facturas table', db_user, db_user_ip;

            RAISE NOTICE 'Updating row in facturas table';
            INSERT INTO factura_audits (old_data, new_data, db_user, db_user_ip, execution_time)
            VALUES (row_to_json(OLD), row_to_json(NEW), db_user, db_user_ip, execution_time);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
