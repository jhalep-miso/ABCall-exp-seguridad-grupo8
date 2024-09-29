import psycopg2
import time
import hashlib, secrets
from datetime import datetime
from celery import Celery

celery_app = Celery(__name__, broker='redis://redis:6379/0')


@celery_app.task(name='notify_integrity_check')
def notify_integrity_check(*args):
    pass


integrity_log_queue = 'integrity_log'


def verify_checksum(new_data):
    monto_str = f"{float(new_data['monto']):.2f}"
    fecha_str = datetime.strptime(new_data['fecha'], '%Y-%m-%dT%H:%M:%S.%f').strftime(
        '%Y-%m-%dT%H:%M:%S.%f'
    )
    data = f'{new_data["id"]}{new_data["usuario_id"]}{new_data["nombre"]}{monto_str}{new_data["detalle"]}{new_data["estado"]}{fecha_str}'
    data_checksum = new_data["checksum"]
    calculated_checksum = hashlib.sha256(data.encode('utf-8')).hexdigest()
    return secrets.compare_digest(data_checksum, calculated_checksum)


def process_audit(old_data, new_data):
    return verify_checksum(new_data)


def main():
    print("Starting listener...")
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="db",
    )
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    while True:
        cursor.execute(
            '''
            select id, factura_id, old_data, new_data, db_user, db_user_ip, execution_time
            from factura_audits
            where processed = false
            '''
        )
        factura_audits = cursor.fetchall()

        for audit in factura_audits:
            (
                audit_id,
                factura_id,
                old_data,
                new_data,
                db_user,
                db_user_ip,
                execution_time,
            ) = audit
            is_valid_checksum = process_audit(old_data, new_data)
            cursor.execute(
                "UPDATE factura_audits SET processed = TRUE, is_valid_checksum=%s WHERE id = %s",
                (
                    is_valid_checksum,
                    audit_id,
                ),
            )
            conn.commit()
            args = (
                audit_id,
                factura_id,
                old_data,
                new_data,
                is_valid_checksum,
                db_user,
                db_user_ip,
                execution_time,
            )
            notify_integrity_check.apply_async(args=args, queue=integrity_log_queue)

        time.sleep(2)


if __name__ == "__main__":
    main()
