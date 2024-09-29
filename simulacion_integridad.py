import requests
from faker import Faker
import random
import logging
import pytz
import datetime
import time

from plot import generar_grafico

fake = Faker()

TIME_ZONE = 'UTC'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

timezone = pytz.timezone(TIME_ZONE)
facturas_url = 'http://localhost:5053/facturas'
auth_url = 'http://localhost:5053/auth'


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


def crear_usuario(username, password):
    data = {
        'username': username,
        'password': password,
    }
    response = requests.post(f'{auth_url}/register', json=data)
    result = response.json()
    print(result)
    return data


def login(username, password):
    data = {
        'username': username,
        'password': password,
    }
    response = requests.post(f'{auth_url}/login', json=data)
    result = response.json()
    return result['token']


def crear_facturas(token, cantidad=10):
    factura_ids = []

    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    for i in range(cantidad):
        data = {
            'usuario_id': 1,
            'nombre': fake.word(),
            'detalle': fake.sentence(),
            'monto': fake.random_int(min=1000, max=10000),
        }
        response = requests.post(facturas_url, json=data, headers=headers)
        result = response.json()
        factura_id = result['factura_id']
        factura_ids.append(factura_id)
        print(f'Factura creada con id {factura_id}')

    return factura_ids


def actualizar_factura(token, factura_id, checksum_ok=True):
    url = (
        f'{facturas_url}/{factura_id}'
        if checksum_ok
        else f'{facturas_url}/{factura_id}/no-checksum'
    )
    data = {
        'nombre': fake.word(),
        'detalle': fake.sentence(),
        'monto': fake.random_int(min=1000, max=10000),
    }
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    requests.put(url, json=data, headers=headers)


def main():
    cantidad_facturas = 4
    cantidad_modificaciones = 200
    username = fake.user_name()
    password = fake.password()
    crear_usuario(username, password)
    token = login(username, password)

    factura_ids = crear_facturas(token, cantidad_facturas)
    for i in range(cantidad_modificaciones):
        factura_id = random.choice(factura_ids)
        with_checksum_ok = random.choice([True, False])
        logger.info(
            f'Actualización Factura {i+1} - factura_id {factura_id} - checksum {with_checksum_ok}'
        )
        actualizar_factura(token, factura_id, checksum_ok=with_checksum_ok)
        time.sleep(0.1)

    print('Simulación de modificaciones finalizada. Generando gráfico...')
    # dar tiempo para que se generen los logs faltantes
    time.sleep(3)
    generar_grafico()


if __name__ == "__main__":
    main()
