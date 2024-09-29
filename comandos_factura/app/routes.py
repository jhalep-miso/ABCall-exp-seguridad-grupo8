from app import app, db
from .models import Factura
import datetime
from flask import request, jsonify
import logging

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def hello_world():
    facturas = Factura.query.all()
    return [factura.id for factura in facturas]


@app.route('/facturas', methods=['POST'])
def crear_factura():
    data = request.json
    factura = Factura(
        usuario_id=data['usuario_id'],
        nombre=data['nombre'],
        monto=data['monto'],
        detalle=data['detalle'],
        estado='pendiente',
        fecha=datetime.datetime.now(),
    )
    factura.checksum = factura.calcular_checksum()
    db.session.add(factura)
    db.session.commit()
    factura_id = factura.id
    return jsonify({"message": "Factura creada", "factura_id": factura_id}), 201


@app.route('/facturas/<int:factura_id>', methods=['PUT'])
def actualizar_factura(factura_id):
    data = request.json
    factura = Factura.query.get_or_404(factura_id)
    factura.usuario_id = data.get('usuario_id', factura.usuario_id)
    factura.nombre = data.get('nombre', factura.nombre)
    factura.monto = data.get('monto', factura.monto)
    factura.detalle = data.get('detalle', factura.detalle)
    factura.estado = data.get('estado', factura.estado)
    factura.checksum = factura.calcular_checksum()
    db.session.commit()
    return f'Factura actualizada {factura.id}'
