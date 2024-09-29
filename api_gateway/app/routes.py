from flask import Blueprint, request, jsonify, Flask
import requests
from functools import wraps
import jwt

gateway_bp = Blueprint('gateway', __name__)


SECRET_KEY = 'a4f809f6b3e2fa6e1d9f4c79f40f6b2e8e6f9e4f4c3b6e8b9f5f4e9f8f4f6f3f'
FACTURAS_SERVICE_URL = "http://comandos_factura:5051"


def token_required(f):
    @wraps(f)
    def decorator_wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            token = token.split()[1]
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid!"}), 401
        return f(user_id=user_id, *args, **kwargs)
    return decorator_wrapper



@gateway_bp.route('/protected', methods=['GET'])
@token_required
def protected_route():
    return jsonify({"message": "This is a protected route"}), 200


# Rutas del API Gateway
@gateway_bp.route('/')
def hello_world():
    response = requests.get(f"{FACTURAS_SERVICE_URL}/")
    return response.json(), response.status_code


@gateway_bp.route('/facturas', methods=['POST'])
@token_required
def crear_factura(user_id):
    data = request.json

    data['usuario_id'] = user_id

    response = requests.post(f"{FACTURAS_SERVICE_URL}/facturas", json=data)
    return response.json(), response.status_code



@gateway_bp.route('/facturas/<int:factura_id>', methods=['PUT'])
@token_required
def actualizar_factura(user_id, factura_id):
    data = request.json

    data['usuario_id'] = user_id

    response = requests.put(f"{FACTURAS_SERVICE_URL}/facturas/{factura_id}", json=data)
    return response.json(), response.status_code



