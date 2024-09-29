import jwt
from app import app, db
from .models import Factura
import datetime
from flask import request, jsonify
import logging

logging.basicConfig(level=logging.DEBUG)

SECRET_KEY = 'aP9fG7kH1jL3mN6pQ2rT8vX4zY5dE1wR9sU0oK7vZ3lF6qB'


@app.route('/')
def hello_world():
    facturas = Factura.query.all()
    return [factura.id for factura in facturas]


@app.before_request
def before_request():
    response = verify_service_token()
    if response:
        return response


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
    return {
        'factura_id': factura.id,
    }, 200


# endpoint sintético para actualizar una factura sin calcular el checksum
@app.route('/facturas/<int:factura_id>/no-checksum', methods=['PUT'])
def actualizar_factura_no_checksum(factura_id):
    data = request.json
    factura = Factura.query.get_or_404(factura_id)
    factura.usuario_id = data.get('usuario_id', factura.usuario_id)
    factura.nombre = data.get('nombre', factura.nombre)
    factura.monto = data.get('monto', factura.monto)
    factura.detalle = data.get('detalle', factura.detalle)
    factura.estado = data.get('estado', factura.estado)
    db.session.commit()
    return {
        'factura_id': factura.id,
    }, 200


@app.route('/facturas/mis-facturas', methods=['GET'])
def obtener_facturas_usuario():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({"message": "Token faltante"}), 401

    token = auth_header.split(" ")[1]

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token['user_id']

        facturas = Factura.query.filter_by(usuario_id=user_id).all()
        if not facturas:
            return (
                jsonify({"message": "No se encontraron facturas para este usuario"}),
                404,
            )

        facturas_json = [
            {
                "id": f.id,
                "nombre": f.nombre,
                "monto": f.monto,
                "detalle": f.detalle,
                "estado": f.estado,
            }
            for f in facturas
        ]

        return jsonify({"facturas": facturas_json}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token vencido"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token no válido"}), 401


def verify_service_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return (
            jsonify(
                {
                    "message": "No ingresar directamente al servicio - Falta agregar el autorizador en los headers"
                }
            ),
            403,
        )

    try:
        token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if decoded_token['service'] != 'api_gateway':
            return jsonify({"message": "No ingresar directamente al servicio"}), 403
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token vencido"}), 403
    except jwt.InvalidTokenError:
        return (
            jsonify(
                {"message": "Token no valido - No ingresar directamente al servicio"}
            ),
            403,
        )
