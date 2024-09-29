import requests
from faker import Faker
import random

fake = Faker()


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
        print(
            f'Factura {factura_id} actualizada con checksum {"OK" if with_checksum_ok else "incorrecto"}'
        )


if __name__ == "__main__":
    main()
