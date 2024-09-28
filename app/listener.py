import psycopg2
import time


def process_audit(old_data, new_data):
    print(f"Processing factura_audits: {old_data} - {new_data}")


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
            process_audit(old_data, new_data)
            cursor.execute(
                "UPDATE factura_audits SET processed = TRUE WHERE id = %s",
                (audit_id,),
            )
            conn.commit()

        time.sleep(2)


if __name__ == "__main__":
    main()
