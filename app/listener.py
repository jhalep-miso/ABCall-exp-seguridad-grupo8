import psycopg2
import time
import hashlib, secrets
from datetime import datetime


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
            "SELECT id, old_data, new_data FROM factura_audits WHERE processed = FALSE"
        )
        factura_audits = cursor.fetchall()

        for audit in factura_audits:
            audit_id, old_data, new_data = audit
            is_valid_checksum = process_audit(old_data, new_data)
            print(f"Factura audit {audit_id} checksum is valid: {is_valid_checksum}")
            cursor.execute(
                "UPDATE factura_audits SET processed = TRUE WHERE id = %s",
                (audit_id,),
            )
            conn.commit()

        time.sleep(2)


if __name__ == "__main__":
    main()
