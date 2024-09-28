"""crear trigger update facturas

Revision ID: b7e9450d06e0
Revises: 6a9b289d8a7e
Create Date: 2024-09-27 03:31:08.466014

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7e9450d06e0'
down_revision = '6a9b289d8a7e'
branch_labels = None
depends_on = None


def upgrade():

    op.execute(
        """
    CREATE TABLE factura_audits (
        id SERIAL PRIMARY KEY,
        old_data JSONB NOT NULL,
        new_data JSONB NOT NULL,
        db_user TEXT,
        db_user_ip TEXT,
        execution_time TIMESTAMP,
        processed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """
    )

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

    op.execute(
        """
    CREATE TRIGGER before_update_facturas_trigger
    BEFORE UPDATE ON facturas
    FOR EACH ROW
    EXECUTE FUNCTION before_update_facturas();
    """
    )


def downgrade():
    op.execute(
        """
    DROP TRIGGER IF EXISTS before_update_facturas_trigger ON facturas;
    """
    )

    op.execute(
        """
    DROP FUNCTION IF EXISTS before_update_facturas();
    """
    )

    op.execute(
        """
    DROP TABLE IF EXISTS factura_audits;
    """
    )
