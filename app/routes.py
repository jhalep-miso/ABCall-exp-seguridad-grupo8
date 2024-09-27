from app import app, db
from .models import Factura
import datetime


@app.route('/')
def hello_world():
    facturas = Factura.query.all()
    return [factura.id for factura in facturas]

@app.route('/crear_factura', methods=['POST'])
def crear_factura():
    factura = Factura(
        usuario_id=1,
        nombre='Factura 1',
        monto=100,
        detalle='Detalle de la factura',
        estado='pendiente',
        fecha=datetime.datetime.now()
    )
    db.session.add(factura)
    db.session.commit()
    return f'Factura creada {factura.id}'
