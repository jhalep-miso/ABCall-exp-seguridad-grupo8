from app import db


class Factura(db.Model):
    __tablename__ = 'facturas'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    nombre = db.Column(db.String(128))
    monto = db.Column(db.Float)
    detalle = db.Column(db.String(128))
    estado = db.Column(db.String(128))
    fecha = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Factura {self.id} - {self.nombre} - {self.detalle} - {self.estado}>'
