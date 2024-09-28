from app import db, app
import hashlib


class Factura(db.Model):
    __tablename__ = 'facturas'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    nombre = db.Column(db.String(128))
    monto = db.Column(db.Float)
    detalle = db.Column(db.String(128))
    estado = db.Column(db.String(128))
    fecha = db.Column(db.DateTime)
    checksum = db.Column(db.String(64), nullable=False, server_default='')

    def calcular_checksum(self):
        monto_str = f"{float(self.monto):.2f}"
        fecha_str = self.fecha.strftime('%Y-%m-%dT%H:%M:%S.%f')
        data = f'{self.id}{self.usuario_id}{self.nombre}{monto_str}{self.detalle}{self.estado}{fecha_str}'
        checksum = hashlib.sha256(data.encode('utf-8')).hexdigest()
        return checksum
