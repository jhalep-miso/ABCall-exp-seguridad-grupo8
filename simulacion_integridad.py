import requests
from faker import Faker
import random
import logging
import pytz
import datetime

fake = Faker()

TIME_ZONE = 'UTC'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

timezone = pytz.timezone(TIME_ZONE)


class CustomFormatter(logging.Formatter):
    def converter(self, timestamp):
        dt = datetime.datetime.fromtimestamp(timestamp, tz=timezone)
        return dt

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s


formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s')

# Crear un manejador de archivo para almacenar logs
log_filename = datetime.datetime.now(timezone).strftime(
    'logs/simulacion_modificaciones_%Y%m%d_%H%M%S.log'
)
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Crear un manejador de consola para mostrar logs en terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def crear_facturas(cantidad=10):
    url = 'http://localhost:5000/facturas'
    factura_ids = []
    for i in range(cantidad):
        data = {
            'usuario_id': 1,
            'nombre': fake.word(),
            'detalle': fake.sentence(),
            'monto': fake.random_int(min=1000, max=10000),
        }
        response = requests.post(url, json=data)
        result = response.json()
        factura_ids.append(result['id'])
        print(f'Factura creada con id {result["id"]} y checksum {result["checksum"]}')

    return factura_ids


def actualizar_factura(factura_id, checksum_ok=True):
    url = (
        f'http://localhost:5000/facturas/{factura_id}'
        if checksum_ok
        else f'http://localhost:5000/facturas/{factura_id}/no-checksum'
    )
    data = {
        'nombre': fake.word(),
        'detalle': fake.sentence(),
        'monto': fake.random_int(min=1000, max=10000),
    }
    requests.put(url, json=data)


def main():
    factura_ids = crear_facturas(100)
    for factura_id in factura_ids:
        with_checksum_ok = random.choice([True, False])
        actualizar_factura(factura_id, checksum_ok=with_checksum_ok)
        logger.info(
            f'Actualización Factura - factura_id {factura_id} - checksum {"OK" if with_checksum_ok else "incorrecto"}'
        )


if __name__ == "__main__":
    main()
